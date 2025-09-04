# server/app/embeddings.py
import os
from dotenv import load_dotenv
import logging
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure logger
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBED_DIM = int(os.getenv("EMBED_DIM", "3072"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")

if not (EMBEDDING_MODEL.startswith("models/") or EMBEDDING_MODEL.startswith("tunedModels/")):
    EMBEDDING_MODEL = f"models/{EMBEDDING_MODEL}"

genai.configure(api_key=GOOGLE_API_KEY)


def embed_texts(texts, task_type: str = "retrieval_document"):
    """
    Batch embedding for a list of texts, with safe fallback if Gemini refuses output_dimensionality.
    """
    resp = None
    embeddings = []

    # --- First try with explicit dimensionality ---
    try:
        resp = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=texts,
            task_type=task_type,
            output_dimensionality=EMBED_DIM,
        )
    except TypeError:
        logger.warning("embed_content() raised TypeError with output_dimensionality, retrying without it.")
    except Exception as e:
        logger.error(f"embed_content() failed with dimension={EMBED_DIM}: {e}")

    # --- If no response or embeddings, retry without dimensionality ---
    if not resp:
        try:
            resp = genai.embed_content(
                model=EMBEDDING_MODEL,
                content=texts,
                task_type=task_type,
            )
            logger.warning("Fallback: embed_content() without output_dimensionality worked.")
        except Exception as e:
            logger.error(f"embed_content() failed completely: {e}")
            return []

    # --- Parse response consistently ---
    if hasattr(resp, "embeddings"):
        embeddings = [emb.embedding for emb in resp.embeddings]
    elif isinstance(resp, dict) and "embeddings" in resp:
        embeddings = [e.get("embedding") or e.get("values") for e in resp["embeddings"]]

    if not embeddings:
        logger.error(f"[EmbedTexts] No embeddings returned. raw response={resp}")
        return []

    logger.info(f"[EmbedTexts] model={EMBEDDING_MODEL}, batch={len(texts)}, dim={len(embeddings[0])}")
    return embeddings


def embed_text(text: str, task_type: str = "retrieval_document"):
    """Single text fallback (for convenience)."""
    embs = embed_texts([text], task_type=task_type)
    if not embs:
        return None
    return embs[0]
