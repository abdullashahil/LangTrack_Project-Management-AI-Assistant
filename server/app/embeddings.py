# server/app/embeddings.py
import os
import time
import logging
from dotenv import load_dotenv
import google.generativeai as genai

# Load env
load_dotenv()

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBED_DIM = int(os.getenv("EMBED_DIM", "3072"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")

if not (EMBEDDING_MODEL.startswith("models/") or EMBEDDING_MODEL.startswith("tunedModels/")):
    EMBEDDING_MODEL = f"models/{EMBEDDING_MODEL}"

genai.configure(api_key=GOOGLE_API_KEY)


def embed_text(text: str, task_type: str = "retrieval_document", retries: int = 3, backoff: int = 10):
    """
    Embed a single text with retry logic.
    """
    for attempt in range(retries):
        try:
            resp = genai.embed_content(
                model=EMBEDDING_MODEL,
                content=text,
                task_type=task_type,
                output_dimensionality=EMBED_DIM,
            )
            # Handle response variations
            if hasattr(resp, "embedding"):
                return resp.embedding
            if isinstance(resp, dict) and "embedding" in resp:
                return resp["embedding"]
            logger.warning(f"[EmbedText] Unexpected response: {resp}")
            return None
        except Exception as e:
            if "429" in str(e):
                wait_time = backoff * (2 ** attempt)  # exponential backoff
                logger.warning(f"⚠️ Quota exceeded (429). Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"❌ Embedding error: {e}")
                return None
    logger.error("❌ Max retries reached. Returning None.")
    return None


def embed_texts(texts, task_type: str = "retrieval_document"):
    """
    Safe wrapper: embeds texts one by one (slower, but avoids Gemini API batch issues).
    """
    embeddings = []
    for i, t in enumerate(texts):
        emb = embed_text(t, task_type=task_type)
        if emb:
            embeddings.append(emb)
        else:
            logger.warning(f"⚠️ Skipping text {i}, no embedding returned.")
    logger.info(f"[EmbedTexts] model={EMBEDDING_MODEL}, count={len(embeddings)}, dim={len(embeddings[0]) if embeddings else '??'}")
    return embeddings
