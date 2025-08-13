import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBED_DIM = int(os.getenv("EMBED_DIM", "768"))
EMBEDDING_MODEL = "text-embedding-004"

genai.configure(api_key=GOOGLE_API_KEY)

def embed_text(text: str, task_type="retrieval_document"):
    res = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type=task_type,
        output_dimensionality=EMBED_DIM,
    )
    return res["embedding"]
