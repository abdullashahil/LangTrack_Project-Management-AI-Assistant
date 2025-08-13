import os
import uuid
import pandas as pd
from app.pinecone_client import get_index
from app.embeddings import embed_text
from app.rag_utils import chunk_text

# Direct CSV URL (replace spaces with %20)
CSV_URL = "https://huggingface.co/datasets/JohnVans123/ProjectManagement/resolve/main/Project%20Management%20(2).csv"

def ingest_dataset():
    print("Downloading dataset from Hugging Face CSV...")
    df = pd.read_csv(CSV_URL)

    index = get_index()
    records = []

    for _, row in df.iterrows():
        # Combine fields into a single text block
        text_parts = []
        for col in df.columns:
            if pd.notna(row[col]):
                text_parts.append(f"{col}: {row[col]}")
        full_text = "\n".join(text_parts)

        # Chunk the text
        chunks = chunk_text(full_text)
        for i, chunk in enumerate(chunks):
            vec_id = f"{row.get('id', str(uuid.uuid4()))}::chunk{i}"
            emb = embed_text(chunk)
            metadata = {col: str(row[col]) for col in df.columns if pd.notna(row[col])}
            metadata["text"] = chunk
            records.append((vec_id, emb, metadata))

    # Upload to Pinecone
    index.upsert(vectors=records)
    print(f"✅ Ingested {len(records)} chunks into Pinecone.")

if __name__ == "__main__":
    ingest_dataset()
