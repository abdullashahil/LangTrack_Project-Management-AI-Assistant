# server/app/embeddings.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBED_DIM = int(os.getenv("EMBED_DIM", "768"))
# keep backwards compatible default but normalize it below
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-004")

# Normalize model name to the required format: must start with "models/" or "tunedModels/"
if not (EMBEDDING_MODEL.startswith("models/") or EMBEDDING_MODEL.startswith("tunedModels/")):
    EMBEDDING_MODEL = f"models/{EMBEDDING_MODEL}"

genai.configure(api_key=GOOGLE_API_KEY)
logger = logging.getLogger(__name__)



def _extract_embedding(resp):
    """
    Try several common response shapes and return the vector/list of floats.
    """
    if resp is None:
        raise ValueError("embed response is None")

    # common (your original): {"embedding": [...]}
    if isinstance(resp, dict) and "embedding" in resp:
        return resp["embedding"]

    # other common shapes:
    # {"embeddings": [{"embedding": [...]}]} or {"embeddings": [{"vector": [...]}, ...]}
    if isinstance(resp, dict) and "embeddings" in resp:
        embs = resp["embeddings"]
        if embs and isinstance(embs, list):
            first = embs[0]
            if isinstance(first, dict):
                for key in ("embedding", "vector", "value"):
                    if key in first:
                        return first[key]
                # some libs place vector under "embedding" -> "embedding"
                if "embedding" in first and isinstance(first["embedding"], dict) and "value" in first["embedding"]:
                    return first["embedding"]["value"]

    # google.genai (newer client) sometimes returns an object with attribute .embedding or .embeddings
    try:
        # handle objects with attributes
        if hasattr(resp, "embedding"):
            return resp.embedding
        if hasattr(resp, "embeddings"):
            embs = resp.embeddings
            if embs and hasattr(embs[0], "embedding"):
                return embs[0].embedding
    except Exception:
        pass

    # if nothing matched, raise with debug info
    raise ValueError(f"Unknown embed response shape: {type(resp)}; repr: {repr(resp)[:1024]}")


def embed_text(text: str, task_type: str = "retrieval_document"):
    """
    Call genai embed API in a way that works across SDK versions:
     - first try the call including output_dimensionality (older code)
     - if that fails due to API signature, call without it
    Returns: list[float] embedding vector
    """
    try:
        # Try original call (works with some sdks)
        resp = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type=task_type,
            output_dimensionality=EMBED_DIM,
        )
    except TypeError as e:
        # SDK doesn't accept output_dimensionality: retry without it
        logger.info("embed_content() doesn't accept output_dimensionality; retrying without that arg.")
        resp = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type=task_type,
        )
    except Exception as e:
        # other errors: re-raise after logging
        logger.exception("Unexpected error calling embed_content")
        raise

    # extract vector from response
    emb = _extract_embedding(resp)
    return emb
