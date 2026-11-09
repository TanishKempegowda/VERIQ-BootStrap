# services/hindsight_service.py
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BASE_URL = "https://api.hindsight.vectorize.io"
MEMORY_BANK_ID = os.getenv("HINDSIGHT_MEMORY_BANK", "veriq-abc-tech")

# Initialize the client
client = Hindsight(
    base_url=HINDSIGHT_BASE_URL,
    api_key=HINDSIGHT_API_KEY
)

def retain_memory(finding_text, metadata=None):
    """Saves a verified finding into Hindsight memory."""
    try:
        client.retain(
            bank_id=MEMORY_BANK_ID,
            content=finding_text,
            metadata=metadata or {}
        )
        return {"status": "success", "message": "Memory retained successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def recall_memory(query_text, limit=3):
    """Recalls similar findings from Hindsight memory."""
    try:
        response = client.recall(
            bank_id=MEMORY_BANK_ID,
            query=query_text
        )
        
        results = []
        for mem in response.results[:limit]:
            results.append({
                "content": mem.text,
                "similarity_score": getattr(mem, 'score', 0.0)
            })
            
        return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}