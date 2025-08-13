from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from google.api_core import retry
import os
from dotenv import load_dotenv
import time
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from app.pinecone_client import get_index
from app.embeddings import embed_text
from app.rag_utils import build_prompt

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://langtrack-project-assistant.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
llm = genai.GenerativeModel("gemini-1.5-flash")

class Query(BaseModel):
    question: str

def generate_with_retry(prompt: str, max_retries: int = 3, delay: int = 2) -> str:
    """
    Retry wrapper for llm.generate_content
    """
    for attempt in range(1, max_retries + 1):
        try:
            response = llm.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                raise HTTPException(status_code=500, detail=f"Failed after {max_retries} attempts: {e}")
            time.sleep(delay)

@app.post("/ask")
async def ask_question(query: Query):
    index = get_index()
    q_emb = embed_text(query.question, task_type="retrieval_query")
    print(q_emb)
    res = index.query(vector=q_emb, top_k=6, include_metadata=True)
    print(res)
    contexts = [match["metadata"]["text"] for match in res.matches]
    print(contexts)
    prompt = build_prompt(query.question, contexts)
    
    # Use retry mechanism
    answer = generate_with_retry(prompt)
    
    return {
        "success": True,
        "data": {
            "answer": answer
        }
    }

@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "ok", "version": "1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
