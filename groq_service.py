# services/groq_service.py
import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load the API key from .env
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_policy_text(policy_text):
    """Sends the policy text to Llama 3 to extract requirements."""
    
    prompt = f"""
    You are an expert compliance auditor. Read the following policy text and extract the core compliance rules.
    Return the result as a valid JSON array of strings. Do not include any other text outside the JSON.
    
    Example format: ["Requirement 1", "Requirement 2"]
    
    Policy Text:
    {policy_text}
    """
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile", # The most reliable free model on Groq
            temperature=0.1, # Keep it strict (low creativity)
        )
        
        # Extract the string response
        raw_output = response.choices[0].message.content
        return raw_output
        
    except Exception as e:
        return f"Error connecting to Groq: {str(e)}"