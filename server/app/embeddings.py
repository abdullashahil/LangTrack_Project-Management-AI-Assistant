# server/app/embeddings.py
import os
from dotenv import load_dotenv
import logging
import google.generativeai as genai

load_dotenv()
logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBED_DIM = int(os.getenv("EMBED_DIM", "768"))

# Prefer explicit full model id set in the environment; fall back to a known-good default
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")

# ensure model string at least begins correctly (defensive)
if not (EMBEDDING_MODEL.startswith("models/") or EMBEDDING_MODEL.startswith("tunedModels/")):
    EMBEDDING_MODEL = f"models/{EMBEDDING_MODEL}"

genai.configure(api_key=GOOGLE_API_KEY)


def _extract_embedding(resp):
    if resp is None:
        raise ValueError("embed response is None")

    if isinstance(resp, dict) and "embedding" in resp:
        return resp["embedding"]

    if isinstance(resp, dict) and "embeddings" in resp:
        embs = resp["embeddings"]
        if embs and isinstance(embs, list):
            first = embs[0]
            if isinstance(first, dict):
                for key in ("embedding", "vector", "value"):
                    if key in first:
                        return first[key]
                if "embedding" in first and isinstance(first["embedding"], dict) and "value" in first["embedding"]:
                    return first["embedding"]["value"]

    # try attribute-style (some client objects)
    if hasattr(resp, "embedding"):
        return getattr(resp, "embedding")
    if hasattr(resp, "embeddings"):
        embs = getattr(resp, "embeddings")
        if embs and hasattr(embs[0], "embedding"):
            return embs[0].embedding

    raise ValueError(f"Unknown embed response shape: {type(resp)}; repr: {repr(resp)[:1024]}")


def embed_text(text: str, task_type: str = "retrieval_document"):
    """
    Robust embedding call:
      - uses EMBEDDING_MODEL env var (fallback to models/gemini-embedding-001)
      - handles SDKs that reject output_dimensionality
      - logs errors and returns a vector or raises a clear exception
    """
    last_exc = None
    model = EMBEDDING_MODEL

    # Try calling with output_dimensionality first (for older SDK shapes)
    try:
        resp = genai.embed_content(
            model=model,
            content=text,
            task_type=task_type,
            output_dimensionality=EMBED_DIM,
        )
    except TypeError as e:
        # the client doesn't accept output_dimensionality -> retry without it
        logger.info("embed_content() doesn't accept output_dimensionality; retrying without it.")
        try:
            resp = genai.embed_content(
                model=model,
                content=text,
                task_type=task_type,
            )
        except Exception as e2:
            last_exc = e2
            logger.exception("Failed to get embedding without output_dimensionality")
            raise RuntimeError(f"Failed to get embedding (model={model}): {e2}") from e2
    except Exception as e:
        last_exc = e
        logger.exception("Failed to get embedding with output_dimensionality")
        raise RuntimeError(f"Failed to get embedding (model={model}): {e}") from e

    emb = _extract_embedding(resp)
    return emb

print(f"[Startup] EMBEDDING_MODEL in use: {EMBEDDING_MODEL}")
print(f"[Startup] EMBED_DIM in use: {EMBED_DIM}")