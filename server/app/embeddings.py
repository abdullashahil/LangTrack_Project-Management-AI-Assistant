# server/app/embeddings.py
import os
from typing import List, Optional

# use google-genai client
from google import genai
from google.genai import types

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
EMBED_DIM = int(os.getenv("EMBED_DIM", "768"))

_client: Optional[genai.Client] = None

def _get_client() -> genai.Client:
    global _client
    if _client is None:
        # lazy init so import doesn't block startup
        _client = genai.Client(api_key=GOOGLE_API_KEY)
    return _client

def embed_text(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> List[float]:
    """
    Returns embedding vector as plain Python list.
    """
    client = _get_client()
    # use a list of contents so response is consistent
    resp = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=[text],
        config=types.EmbedContentConfig(
            output_dimensionality=EMBED_DIM,
            task_type=task_type,
        ),
    )
    # resp.embeddings[0] may have .values or .embedding depending on SDK - prefer .values
    emb_obj = resp.embeddings[0]
    vector = getattr(emb_obj, "values", None) or getattr(emb_obj, "embedding", None)
    if vector is None:
        # fallback: try the raw dict path if SDK returns mapping
        try:
            return resp["embeddings"][0]["values"]
        except Exception:
            raise RuntimeError("Unexpected embedding response shape: %r" % (resp,))
    return list(vector)
