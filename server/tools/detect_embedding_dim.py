# tools/detect_embedding_dim.py
import os
from dotenv import load_dotenv
from app.embeddings import embed_text
load_dotenv()

def main():
    sample = "Hello, what dimension does this embedding return?"
    emb = embed_text(sample, task_type="retrieval_query")
    print("Detected embedding length:", len(emb))

if __name__ == "__main__":
    main()
