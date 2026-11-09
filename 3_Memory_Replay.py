import streamlit as st
import sys
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

project_path = r"C:\Users\mypcb\OneDrive\VERIQ"
if project_path not in sys.path:
    sys.path.insert(0, project_path)

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

st.markdown("""
<div style="display: flex; align-items: center; gap: 20px; margin-bottom: 30px;">
    <div style="background: #a855f7; padding: 10px 20px; border-radius: 12px; font-size: 24px; font-weight: 700; color: white;">W1</div>
    <div>
        <h1 style="font-size: 32px; font-weight: 700; color: white; margin: 0;">Audit Memory Replay</h1>
    </div>
</div>
""", unsafe_allow_html=True)

query = st.text_input("Search for a finding", "Employee access removal delay")
if st.button("🧠 Recall from Hindsight"):
    with st.spinner("Querying Hindsight memory..."):
        result = recall_from_hindsight(query)
    if result['status'] == 'error': st.error(f"Hindsight error: {result['message']}")
    elif not result['results']: st.warning("🧠 No relevant memory found.")
    else:
        st.success(f"Found {len(result['results'])} relevant memories!")
        for i, mem in enumerate(result['results']):
            st.markdown(f"""
            <div class="glass-panel" style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: white;">📄 Memory #{i+1}</h4>
                </div>
                <p style="color: #ccc; font-size: 14px; margin-top: 10px; white-space: pre-wrap;">{mem['content']}</p>
            </div>
            """, unsafe_allow_html=True)