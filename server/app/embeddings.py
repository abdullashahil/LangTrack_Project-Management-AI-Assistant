# embeddings.py (google-genai)
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBED_DIM = int(os.getenv("EMBED_DIM", "768"))
# recommended embeddings: "gemini-embedding-001" or "text-embedding-005" etc.
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")

# create client (the SDK reads API key env var, or pass it explicitly)
client = genai.Client(api_key=GOOGLE_API_KEY)

def embed_text(text: str, task_type: str = "RETRIEVAL_DOCUMENT"):
    resp = client.models.embed_content(
        model=EMBEDDING_MODEL,
        # contents can be a single string or list of strings
        contents=[text],
        # put the dimensionality & task type in the config object
        config=types.EmbedContentConfig(
            output_dimensionality=EMBED_DIM,
            task_type=task_type,
        ),
    )
    # response has `embeddings` list; each embedding object usually exposes `.values`
    embedding_obj = resp.embeddings[0]
    vector = getattr(embedding_obj, "values", None) or getattr(embedding_obj, "embedding", None)
    return vector
