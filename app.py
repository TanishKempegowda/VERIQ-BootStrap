import streamlit as st
import os
import base64
import plotly.graph_objects as go
from dotenv import load_dotenv
from database.db import init_db, get_connection

load_dotenv()
init_db()

st.set_page_config(page_title="VERIQ Dashboard", layout="wide", initial_sidebar_state="expanded")

# 🔧 Read local bg.jpg and bake it into CSS
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

bg_base64 = get_base64_of_bin_file('bg.jpg')
bg_css = f"""
<style>
.stApp {{
    background-image: 
        linear-gradient(rgba(5, 5, 10, 0.75), rgba(5, 5, 10, 0.85)), 
        url('data:image/jpeg;base64,{bg_base64}') !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    font-family: 'Inter', sans-serif;
}}
[data-testid="stAppViewContainer"] {{ background: transparent !important; }}
[data-testid="stHeader"] {{ background: transparent !important; }}
#MainMenu {{ visibility: hidden !important; }}
footer {{ visibility: hidden !important; }}

/* SIDEBAR */
[data-testid="stSidebar"] {{
    background: rgba(15, 15, 20, 0.6) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
}}
[data-testid="stSidebarNav"] {{ display: none !important; }}
[data-testid="stSidebarUserContent"] {{
    padding-top: 1rem !important;
    display: flex;
    flex-direction: column;
    height: 100%;
}}
[data-testid="stPageLink-NavLink"] {{
    padding: 14px 16px !important;
    border-radius: 10px;
    margin-bottom: 8px;
    background: rgba(255, 255, 255, 0.03);
}}
[data-testid="stPageLink-NavLink"]:hover {{
    background: rgba(255, 255, 255, 0.1);
}}
[data-testid="stPageLink-NavLink"] p {{
    font-size: 17px !important;
    font-weight: 600 !important;
}}
[data-testid="stSidebarUserContent"] > div:last-child {{
    margin-top: auto;
    margin-bottom: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 20px;
}}

/* GLASS CARDS */
.glass-panel {{
    background: rgba(25, 25, 35, 0.4) !important;
    backdrop-filter: blur(24px) saturate(150%) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5) !important;
    margin-bottom: 15px !important;
    color: white;
}}
.kpi-card {{
    display: flex;
    flex-direction: column;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(24px) saturate(150%);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    color: white;
    height: 160px;
    justify-content: space-between;
}}
.kpi-blue {{ background: linear-gradient(135deg, rgba(59, 130, 246, 0.25) 0%, rgba(20, 20, 30, 0.4) 100%); border-left: 3px solid #3b82f6; }}
.kpi-yellow {{ background: linear-gradient(135deg, rgba(234, 179, 8, 0.25) 0%, rgba(20, 20, 30, 0.4) 100%); border-left: 3px solid #eab308; }}
.kpi-green {{ background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(20, 20, 30, 0.4) 100%); border-left: 3px solid #10b981; }}
.kpi-red {{ background: linear-gradient(135deg, rgba(239, 68, 68, 0.25) 0%, rgba(20, 20, 30, 0.4) 100%); border-left: 3px solid #ef4444; }}
.kpi-title {{ font-size: 15px; color: #eee; margin: 0; display: flex; align-items: center; gap: 8px; }}
.kpi-value {{ font-size: 48px; font-weight: 800; margin: 0; color: white; line-height: 1; }}
.kpi-trend {{ font-size: 13px; color: #10b981; margin: 0; }}
.js-plotly-plot .plotly .main-svg {{ background: transparent !important; }}

/* CUSTOM BUTTONS FOR QUICK ACTIONS */
.action-btn {{
    display: block;
    text-align: center;
    padding: 12px;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none !important;
    margin-bottom: 12px;
    transition: all 0.2s;
}}
.action-btn-primary {{
    background: #3b82f6;
    color: white !important;
}}
.action-btn-primary:hover {{
    background: #2563eb;
}}
.action-btn-secondary {{
    background: rgba(255, 255, 255, 0.1);
    color: white !important;
}}
.action-btn-secondary:hover {{
    background: rgba(255, 255, 255, 0.2);
}}
</style>
"""
st.markdown(bg_css, unsafe_allow_html=True)

# --- SIDEBAR ---
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

# --- HEADER ---
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
    <div style="display: flex; align-items: center; gap: 15px;">
        <div style="background: #6366f1; padding: 8px 15px; border-radius: 10px; font-size: 20px; font-weight: 700; color: white;">G1</div>
        <h1 style="margin: 0; font-size: 32px; font-weight: 800; color: white;">Compliance Dashboard</h1>
    </div>
</div>
""", unsafe_allow_html=True)

# --- FETCH DATA ---
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM policies")
total_policies = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM findings")
total_findings = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM findings WHERE severity = 'Gap'")
total_gaps = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM findings WHERE severity = 'Compliant'")
total_compliant = cursor.fetchone()[0]
conn.close()

compliance_rate = int((total_compliant / total_findings) * 100) if total_findings > 0 else 0

# --- ROW 1 ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <a href="/Document_Analysis" target="_self" style="text-decoration: none; color: inherit;">
        <div class="kpi-card kpi-blue">
            <p class="kpi-title">📊 Active Audits</p>
            <h2 class="kpi-value">{total_policies}</h2>
            <p class="kpi-trend">Policies Uploaded</p>
        </div>
    </a>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <a href="/Gap_Detection" target="_self" style="text-decoration: none; color: inherit;">
        <div class="kpi-card kpi-yellow">
            <p class="kpi-title">⚠️ Risk Items</p>
            <h2 class="kpi-value">{total_gaps}</h2>
            <p class="kpi-trend" style="color: #eab308;">Gaps Detected</p>
        </div>
    </a>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <a href="/Memory_Replay" target="_self" style="text-decoration: none; color: inherit;">
        <div class="kpi-card kpi-green">
            <p class="kpi-title">🛡️ Compliance Rate</p>
            <h2 class="kpi-value">{compliance_rate}%</h2>
            <p class="kpi-trend">Based on AI checks</p>
        </div>
    </a>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <a href="/Gap_Detection" target="_self" style="text-decoration: none; color: inherit;">
        <div class="kpi-card kpi-red">
            <p class="kpi-title">❌ Total Findings</p>
            <h2 class="kpi-value">{total_findings}</h2>
            <p class="kpi-trend" style="color: #ef4444;">Requires attention</p>
        </div>
    </a>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- ROW 2 ---
col_left, col_right = st.columns([2, 1])

with col_left:
    # Native Streamlit container with custom CSS class injection
    st.markdown('<div class="glass-panel" style="padding: 24px;"><h3 style="color:white; margin:0 0 20px 0; font-size:18px;">📊 Risk Assessment Overview</h3>', unsafe_allow_html=True)
    chart_c1, chart_c2 = st.columns(2)
    with chart_c1:
        fig_pie = go.Figure(data=[go.Pie(labels=['High', 'Medium', 'Low'], values=[60, 30, 10], hole=0.6, marker_colors=['#3b82f6', '#6366f1', '#1e293b'], textinfo='none')])
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0), height=200, showlegend=False)
        st.plotly_chart(fig_pie, width='stretch')
        st.markdown("<div style='text-align:center; margin-top:-110px; color:white; font-size:24px; font-weight:bold;'>60%</div>", unsafe_allow_html=True)
    with chart_c2:
        fig_bar = go.Figure(data=[go.Bar(x=['May', 'Jun', 'Jul'], y=[100, 150, 120], marker_color=['#3b82f6', '#a855f7', '#10b981'])])
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#aaa', margin=dict(t=20,b=0,l=0,r=0), height=200, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        st.plotly_chart(fig_bar, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # Pure HTML for the whole card so Streamlit doesn't break it
    st.markdown("""
    <div class="glass-panel" style="height: 280px;">
        <h3 style="color:white; margin:0 0 20px 0; font-size:18px;">⚡ Quick Actions</h3>
        <a href="/Document_Analysis" target="_self" class="action-btn action-btn-primary">+ New Audit</a>
        <a href="/Gap_Detection" target="_self" class="action-btn action-btn-secondary">Risk Assessment</a>
        <a href="/Memory_Replay" target="_self" class="action-btn action-btn-secondary">View Reports</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- ROW 3 ---
col_bottom_left, col_bottom_right = st.columns([2, 1])
with col_bottom_left:
    st.markdown("""
    <div class="glass-panel" style="height: 220px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h3 style="color:white; margin:0; font-size:18px;">📋 Operations Audit Progress</h3>
            <span style="background: #1e3a8a; color: #93c5fd; padding: 4px 8px; border-radius: 4px; font-size: 12px;">In Progress</span>
        </div>
        <div style="display: flex; justify-content: space-between; color: #ccc; font-size: 14px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 10px; margin-bottom: 10px;">
            <span>Financial Services</span> <span>Started: 2026-02-21</span> <span style="color: #3b82f6;">14%</span>
        </div>
        <div style="display: flex; justify-content: space-between; color: #ccc; font-size: 14px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 10px; margin-bottom: 10px;">
            <span>Human Resources</span> <span>Completed: 2026-01-18</span> <span style="color: #10b981;">100%</span>
        </div>
        <div style="display: flex; justify-content: space-between; color: #ccc; font-size: 14px;">
            <span>Customer Support</span> <span>Started: 2026-03-01</span> <span style="color: #a855f7;">56%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_bottom_right:
    st.markdown("""
    <div class="glass-panel" style="height: 220px;">
        <h3 style="color:white; margin:0 0 15px 0; font-size:18px;">🛡️ Policy Adherence</h3>
        <div style="display: flex; height: 35px; border-radius: 6px; overflow: hidden; margin-bottom: 15px;">
            <div style="background: #3b82f6; width: 65%; display: flex; align-items: center; justify-content: center; color: white; font-size: 13px; font-weight: bold;">65%</div>
            <div style="background: #eab308; width: 20%; display: flex; align-items: center; justify-content: center; color: white; font-size: 13px; font-weight: bold;">20</div>
            <div style="background: #ef4444; width: 15%; display: flex; align-items: center; justify-content: center; color: white; font-size: 13px; font-weight: bold;">15</div>
        </div>
        <p style="color: #aaa; font-size: 13px; margin: 0;">● 62% Achieving</p>
        <p style="color: #aaa; font-size: 13px; margin: 5px 0 0 0;">● 20% Partial</p>
        <p style="color: #aaa; font-size: 13px; margin: 5px 0 0 0;">● 15% Non-Adhering</p>
    </div>
    """, unsafe_allow_html=True)