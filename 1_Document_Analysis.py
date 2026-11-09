import streamlit as st
import io
import json
import sys
import os
from pypdf import PdfReader
from groq import Groq
from dotenv import load_dotenv

project_path = r"C:\Users\mypcb\OneDrive\VERIQ"
if project_path not in sys.path:
    sys.path.insert(0, project_path)
from database.db import init_db, get_connection

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

with open("styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PdfReader(io.BytesIO(uploaded_file.read()))
        return "".join([page.extract_text() or "" for page in reader.pages])
    except Exception as e: return f"Error: {e}"

def analyze_policy_text(policy_text):
    prompt = f"Extract core compliance rules as a JSON array of strings. Text: {policy_text[:15000]}"
    try:
        response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="qwen/qwen3.8-27b", temperature=0.1)
        return response.choices[0].message.content
    except Exception as e: return f"Error: {e}"

def save_policy_to_db(name, reqs):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO policies (policy_name, extracted_requirements) VALUES (?, ?)", (name, reqs))
    conn.commit()
    conn.close()

init_db()
st.markdown("<h1 style='color: white;'>📄 Document Analysis</h1>", unsafe_allow_html=True)
st.write("Upload a policy PDF to extract compliance rules.")

if "ai_result" not in st.session_state: st.session_state.ai_result = None
if "file_name" not in st.session_state: st.session_state.file_name = None

uploaded_file = st.file_uploader("Upload Policy PDF", type=["pdf"])
if uploaded_file and st.button("Analyze Policy"):
    if st.session_state.file_name != uploaded_file.name: st.session_state.ai_result = None
    with st.spinner("Extracting..."):
        text = extract_text_from_pdf(uploaded_file)
        raw_ai = analyze_policy_text(text)
        st.session_state.ai_result = raw_ai.replace('```json', '').replace('```', '').strip()
        st.session_state.file_name = uploaded_file.name

if st.session_state.ai_result:
    st.success("Policy analyzed!")
    st.json(st.session_state.ai_result)
    if st.button("💾 Save to Database"):
        save_policy_to_db(st.session_state.file_name, st.session_state.ai_result)
        st.success("Saved! Go to Gap Detection.")
        st.session_state.ai_result = None