# server/tools/check_embed_dim.py
import sys
from pathlib import Path
from dotenv import load_dotenv

# ensure project root (server/) on path so `app` package imports work
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

load_dotenv()

import app.embeddings as emb

def main():
    print("EMBEDDING_MODEL (normalized):", getattr(emb, "EMBEDDING_MODEL", None))
    print("EMBED_DIM (expected):", getattr(emb, "EMBED_DIM", None))
    sample = "Hello — testing embedding dimension"
    try:
        vec = emb.embed_text(sample, task_type="retrieval_query")
    except Exception as e:
        print("embed_text() raised an exception:", repr(e))
        return
    if not isinstance(vec, (list, tuple)):
        print("embed_text returned non-list shape:", type(vec), repr(vec)[:200])
        return
    print("Returned vector length:", len(vec))
    # print a small slice so we can inspect numeric format
    print("First 6 values:", vec[:6])

if __name__ == "__main__":
    main()
