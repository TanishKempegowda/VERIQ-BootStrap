import streamlit as st
import json
import sys
import os
import io
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader
from hindsight_client import Hindsight

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from database.db import init_db, get_connection

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

hs_client = Hindsight(base_url="https://api.hindsight.vectorize.io", api_key=os.getenv("HINDSIGHT_API_KEY"))
hs_bank = os.getenv("HINDSIGHT_MEMORY_BANK", "veriq-abc-tech")

def save_to_hindsight(text, metadata):
    try:
        hs_client.retain(bank_id=hs_bank, content=text, metadata=metadata)
        return {"status": "success"}
    except Exception as e: return {"status": "error", "message": str(e)}

# 🔧 BULLETPROOF CSS LOADER
css_path_1 = os.path.join(root_path, "styles", "main.css")
css_path_2 = os.path.join(root_path, "main.css")
css_path = css_path_1 if os.path.exists(css_path_1) else css_path_2

try:
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 30px;">
        <div style="background: #6366f1; padding: 8px; border-radius: 10px; font-size: 20px;">⚡</div>
        <h2 style="margin: 0; color: white; font-size: 22px; font-weight: 800;">VERIQ</h2>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("app.py", label="Dashboard", icon="🏠")
    st.page_link("pages/1_Document_Analysis.py", label="Document Analysis", icon="📄")
    st.page_link("pages/2_Gap_Detection.py", label="Gap Detection", icon="🔍")
    st.page_link("pages/3_Memory_Replay.py", label="Memory Replay", icon="⏱️")
    st.markdown("""
    <div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="background: #a855f7; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white;">SL</div>
            <div>
                <p style="margin: 0; font-size: 15px; font-weight: 600; color: white;">Sarah Lee</p>
                <p style="margin: 0; font-size: 12px; color: #888;">Audit Team</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def extract_text_from_evidence(file):
    try:
        file_bytes = file.read()
        if file.name.endswith('.pdf'):
            reader = PdfReader(io.BytesIO(file_bytes))
            return "".join([page.extract_text() or "" for page in reader.pages])
        else: return file_bytes.decode("utf-8")
    except Exception as e: return f"Error extracting evidence: {e}"

def detect_gap(rule, evidence):
    prompt = f"Rule: {rule}\nEvidence: {evidence}\nReturn JSON with 'status' (Compliant, Gap, Insufficient Evidence) and 'explanation'."
    try:
        response = groq_client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="qwen/qwen3.8-27b", temperature=0.1)
        return response.choices[0].message.content
    except Exception as e: return f"Error: {e}"

def get_all_policies():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, policy_name, extracted_requirements FROM policies")
    rows = cursor.fetchall()
    conn.close()
    return rows

def save_finding_to_db(audit_id, rule, evidence, result_json):
    conn = get_connection()
    cursor = conn.cursor()
    result = json.loads(result_json)
    cursor.execute("INSERT INTO findings (audit_id, issue_description, severity, evidence, status) VALUES (?, ?, ?, ?, ?)", (audit_id, result.get("explanation", ""), result.get("status", "Unknown"), evidence, "Open"))
    conn.commit()
    conn.close()

init_db()
st.markdown("<h1 style='color: white;'>🔍 Gap Detection</h1>", unsafe_allow_html=True)
st.write("Test company evidence against the rules you extracted.")

policies = get_all_policies()
if not policies:
    st.warning("⚠️ No policies found. Go to Document Analysis first.")
else:
    policy_options = {f"{row['policy_name']}": row for row in policies}
    selected = st.selectbox("Select Policy", list(policy_options.keys()))
    requirements = json.loads(policy_options[selected]['extracted_requirements'])
    
    selected_rule = st.selectbox("Select Rule", requirements)
    st.info(f"**Testing Rule:** {selected_rule}")
    
    st.markdown("### 📎 Provide Evidence")
    evidence_file = st.file_uploader("Upload Evidence (PDF or TXT)", type=["pdf", "txt", "md"])
    evidence_text = st.text_area("OR paste evidence text here:")
    
    if st.button("Run Gap Detection"):
        final_evidence = ""
        if evidence_file is not None:
            final_evidence = extract_text_from_evidence(evidence_file)
            st.success(f"Successfully extracted {len(final_evidence)} characters from {evidence_file.name}")
        elif evidence_text:
            final_evidence = evidence_text
            
        if final_evidence:
            with st.spinner("AI is analyzing the gap..."):
                gap_result = detect_gap(selected_rule, final_evidence)
            try:
                clean_gap = gap_result.replace('```json', '').replace('```', '').strip()
                parsed_gap = json.loads(clean_gap)
                st.session_state.current_finding = {"rule": selected_rule, "evidence": final_evidence, "result": clean_gap, "parsed": parsed_gap}
            except Exception as e: st.error(f"Could not parse AI response: {clean_gap}")
        else:
            st.error("Please upload a file or paste evidence first.")

if "current_finding" in st.session_state:
    finding = st.session_state.current_finding
    if finding['parsed']['status'] == 'Compliant': st.success(f"✅ Status: {finding['parsed']['status']}")
    elif finding['parsed']['status'] == 'Gap': st.error(f"❌ Status: {finding['parsed']['status']}")
    else: st.warning(f"⚠️ Status: {finding['parsed']['status']}")
        
    st.write(f"**AI Explanation:** {finding['parsed']['explanation']}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📌 Log to Database"):
            save_finding_to_db(1, finding['rule'], finding['evidence'], finding['result'])
            st.success("✅ Saved to SQLite!")
    with col2:
        if st.button("🧠 Save to Hindsight Memory"):
            memory_text = f"Rule: {finding['rule']}\nEvidence: {finding['evidence']}\nResult: {finding['parsed']['status']}\nExplanation: {finding['parsed']['explanation']}"
            with st.spinner("Retaining memory..."):
                res = save_to_hindsight(memory_text, {"status": finding['parsed']['status']})
            if res['status'] == 'success': st.success("🧠 Memory saved to Hindsight!")
            else: st.error(f"Hindsight error: {res['message']}")
