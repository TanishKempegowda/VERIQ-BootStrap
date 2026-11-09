# services/pdf_service.py
import fitz  # This is PyMuPDF

def extract_text_from_pdf(uploaded_file):
    """Takes a Streamlit uploaded PDF and returns its text."""
    try:
        # Read the file into memory
        file_bytes = uploaded_file.read()
        
        # Open the PDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        
        text = ""
        for page in doc:
            text += page.get_text()
            
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"