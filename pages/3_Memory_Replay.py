import streamlit as st
import sys
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

load_dotenv()
hs_client = Hindsight(base_url="https://api.hindsight.vectorize.io", api_key=os.getenv("HINDSIGHT_API_KEY"))
hs_bank = os.getenv("HINDSIGHT_MEMORY_BANK", "veriq-abc-tech")

def recall_from_hindsight(query):
    try:
        response = hs_client.recall(bank_id=hs_bank, query=query)
        results = []
        for mem in response.results[:3]:
            results.append({"content": getattr(mem, 'text', getattr(mem, 'content', 'No content')), "similarity_score": getattr(mem, 'score', 0.0)})
        return {"status": "success", "results": results}
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

st.markdown("""
<div style="display: flex; align-items: center; gap: 20px; margin-bottom: 30px;">
    <div style="background: #a855f7; padding: 10px 20px; border-radius: 12px; font-size: 24px; font-weight: 700; color: white;">W1</div>
    <div>
        <h1 style="font-size: 32px; font-weight: 700; color: white; margin: 0;">Audit Memory Replay</h1>
        <p style="color: #a0a0a0; font-size: 15px; margin-top: 5px;">Powered by Hindsight Memory</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("### 🔎 Recall Past Cases")
query = st.text_input("Search for a finding (e.g., 'Employee access removal delay')", "Employee access removal delay")

if st.button("🧠 Recall from Hindsight"):
    with st.spinner("Querying Hindsight memory..."):
        result = recall_from_hindsight(query)
    if result['status'] == 'error':
        st.error(f"Hindsight error: {result['message']}")
    elif not result['results']:
        st.warning("🧠 No relevant memory found. Try saving a finding first.")
    else:
        st.success(f"Found {len(result['results'])} relevant memories!")
        for i, mem in enumerate(result['results']):
            st.markdown(f"""
            <div class="glass-panel" style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: white;">📄 Memory #{i+1}</h4>
                    <span style="background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px;">
                        Similarity: {mem['similarity_score']:.2f}
                    </span>
                </div>
                <p style="color: #ccc; font-size: 14px; margin-top: 10px; white-space: pre-wrap;">{mem['content']}</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div class="glass-panel">
    <h3 style="color: white; margin-top: 0;">🌳 Issue Replay Timeline</h3>
    <div style="display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-top: 20px;">
        <div style="background: rgba(220, 38, 38, 0.15); border: 1px solid #ef4444; padding: 15px; border-radius: 10px; color: white; text-align: center; width: 22%;">
            <div style="font-size: 20px;">⚠️</div><strong style="font-size: 14px;">Issue Identified</strong><br><span style="font-size: 12px; color: #aaa;">Jan 08, 2024</span>
        </div>
        <div style="color: #666; font-size: 20px;">➔</div>
        <div style="background: rgba(234, 179, 8, 0.15); border: 1px solid #eab308; padding: 15px; border-radius: 10px; color: white; text-align: center; width: 22%;">
            <div style="font-size: 20px;">🔍</div><strong style="font-size: 14px;">Root Cause</strong><br><span style="font-size: 12px; color: #aaa;">Jan 10, 2024</span>
        </div>
        <div style="color: #666; font-size: 20px;">➔</div>
        <div style="background: rgba(59, 130, 246, 0.15); border: 1px solid #3b82f6; padding: 15px; border-radius: 10px; color: white; text-align: center; width: 22%;">
            <div style="font-size: 20px;">🛠️</div><strong style="font-size: 14px;">Corrective Action</strong><br><span style="font-size: 12px; color: #aaa;">Jan 15, 2024</span>
        </div>
        <div style="color: #666; font-size: 20px;">➔</div>
        <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; padding: 15px; border-radius: 10px; color: white; text-align: center; width: 22%;">
            <div style="font-size: 20px;">✅</div><strong style="font-size: 14px;">Closed</strong><br><span style="font-size: 12px; color: #aaa;">Jan 22, 2024</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
