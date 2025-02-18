from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

# Initialize FastAPI app
app = FastAPI()

# Define the request model
class QueryRequest(BaseModel):
    message: str

# Langflow API configuration
BASE_API_URL = "http://127.0.0.1:7860"  # Update this to the actual Langflow host URL if different
FLOW_ID = "4d4f646f-7a75-4f65-9e76-fcd916354f1e"  # Replace with your actual Flow ID
ENDPOINT = FLOW_ID  # Use this if you have a custom endpoint

# Optional tweaks dictionary (modify this as needed)
TWEAKS = {
    "ChatInput-SfKRq": {},
    "ParseData-3G1k6": {},
    "Prompt-q5ywT": {},
    "ChatOutput-V4clg": {},
    "OpenAIEmbeddings-brUa6": {},
    "File-odKjx": {},
    "OpenAIModel-B3L5y": {},
    "AstraDB-Vomh4": {},
    "SplitText-jYb4Y": {},
    "Memory-FzsPv": {},
    "AstraDB-Tw7lY": {}
}

def run_flow(message: str) -> dict:
    """
    Send a message to the Langflow API and get a response.
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": TWEAKS
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_langflow(request: QueryRequest):
    """
    API endpoint to send a message to Langflow and return the response.
    """
    return run_flow(request.message)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Ensure it listens on all interfaces (important for Azure)


