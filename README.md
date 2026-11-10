# ⚡ VERIQ: AI Compliance & Operations Audit Agent
**Don't repeat the same mistakes. Learn from every audit.**

## 🎯 The Problem
Organizations run compliance audits repeatedly, but auditors often forget past findings. Standard audit tools just log errors in a database; they don't help auditors learn from previous resolutions when a similar issue occurs months later.

## 💡 Our Solution
VERIQ is an AI Agent that combines LLM reasoning with **persistent memory**. 
1. **Reads Policies:** Uses Groq (Qwen) to extract strict compliance rules from PDF documents.
2. **Detects Gaps:** Analyzes real-world evidence against those rules to find violations.
3. **Remembers:** Uses **Hindsight Memory** to store verified findings. If a similar issue happens again in the future, VERIQ recalls the past case and helps the auditor identify recurring weaknesses.

# ⚡ VERIQ: AI Compliance & Operations Audit Agent
**🚀 Live Demo:** https://veriq-bootstrap-avttidtfpkvjmfpcjpi2pd.streamlit.app/

## 🏗️ Tech Stack
- **Frontend:** Streamlit (Custom Glassmorphism UI)
- **AI Engine:** Groq API (`qwen/qwen3.8-27b`)
- **Persistent Memory:** Hindsight Cloud SDK
- **Database:** SQLite (for structured audit logs)
- **PDF Parsing:** PyMuPDF / pypdf

## 🚀 How Hindsight Memory is Used
- **Retain:** When an auditor verifies a finding (e.g., an IT access delay), it is saved to the Hindsight vector database.
- **Recall:** When new evidence is analyzed, VERIQ queries Hindsight to see if the organization has made this exact mistake before, pulling up the historical resolution.

## 💻 Local Setup
1. `pip install -r requirements.txt`
2. Create a `.env` file with `GROQ_API_KEY` and `HINDSIGHT_API_KEY`.
3. Run `streamlit run app.py`

## 👥 Team Bootstrap
- First-Year Engineering Students
