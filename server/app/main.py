# server/app/main.py
import os
import time
from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

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

# Lazy globals (do not initialize SDKs at import time)
_llm = None
_index = None

class Query(BaseModel):
    question: str

def get_llm():
    """
    Lazy-init the Gemini LLM client (keeps import-time fast).
    Uses the same google.generativeai API you had locally.
    """
    global _llm
    if _llm is None:
        try:
            import google.generativeai as genai  # local import so startup isn't blocked
        except Exception as e:
            raise RuntimeError("google.generativeai SDK not available: %s" % e)
        # configure per-request / once
        genai.configure(api_key=GOOGLE_API_KEY)
        _llm = genai.GenerativeModel("gemini-1.5-flash")
    return _llm

def get_pinecone_index():
    """
    Lazy import of pinecone client and index. This avoids network calls during import.
    Your app.pinecone_client.get_index should itself avoid heavy work at import.
    """
    global _index
    if _index is None:
        # import inside function
        try:
            from app.pinecone_client import get_index as _get_index  # local import
        except Exception as e:
            raise RuntimeError("Failed to import pinecone client: %s" % e)
        _index = _get_index()
    return _index

def generate_with_retry(prompt: str, max_retries: int = 3, delay: int = 2) -> str:
    """
    Retry wrapper for llm.generate_content
    """
    llm = get_llm()
    for attempt in range(1, max_retries + 1):
        try:
            # call LLM generation
            response = llm.generate_content(prompt)
            # older google.generativeai returns .text
            return response.text.strip()
        except Exception as e:
            print(f"LLM attempt {attempt} failed: {e}")
            if attempt == max_retries:
                raise HTTPException(status_code=500, detail=f"Failed after {max_retries} attempts: {e}")
            time.sleep(delay)


@app.post("/ask")
async def ask_question(query: Query):
    # import embed_text lazily (embeddings.py should be lazy as well)
    try:
        from app.embeddings import embed_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import embeddings: {e}")

    # create / get Pinecone index lazily
    try:
        index = get_pinecone_index()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize Pinecone index: {e}")

    # compute embedding (embeddings.embed_text should not call remote at import time)
    try:
        # use the task_type your embeddings impl expects
        q_emb = embed_text(query.question, task_type="retrieval_query")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get embedding: {e}")

    # query Pinecone
    try:
        res = index.query(vector=q_emb, top_k=6, include_metadata=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pinecone query failed: {e}")

    matches = getattr(res, "matches", None) or res.get("matches", [])  # support different response shapes
    contexts = []
    for match in matches:
        md = match.get("metadata") if isinstance(match, dict) else match.metadata
        if md:
            contexts.append(md.get("text") if isinstance(md, dict) else getattr(md, "text", None))

    # build prompt lazily (should be cheap)
    try:
        from app.rag_utils import build_prompt
        prompt = build_prompt(query.question, contexts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to build prompt: {e}")

    # call LLM with retry
    answer = generate_with_retry(prompt)

    return {"success": True, "data": {"answer": answer}}


@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "ok", "version": "1.0"}
