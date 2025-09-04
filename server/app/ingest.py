# app/ingest.py
import os
import uuid
import pandas as pd
from app.pinecone_client import get_index
from app.embeddings import embed_texts
from app.rag_utils import chunk_text

CSV_URL = "https://huggingface.co/datasets/JohnVans123/ProjectManagement/resolve/main/Project%20Management%20(2).csv"

def ingest_dataset(batch_size: int = 32):
    print("📥 Downloading dataset from Hugging Face CSV...")
    df = pd.read_csv(CSV_URL)

    index = get_index()
    all_chunks, metadata_list, ids = [], [], []

    # Collect chunks
    for _, row in df.iterrows():
        text_parts = [f"{col}: {row[col]}" for col in df.columns if pd.notna(row[col])]
        full_text = "\n".join(text_parts)

        chunks = chunk_text(full_text)
        for i, chunk in enumerate(chunks):
            vec_id = f"{row.get('id', str(uuid.uuid4()))}::chunk{i}"
            meta = {col: str(row[col]) for col in df.columns if pd.notna(row[col])}
            meta["text"] = chunk

            ids.append(vec_id)
            all_chunks.append(chunk)
            metadata_list.append(meta)

    print(f"📊 Total chunks to embed: {len(all_chunks)}")

    records = []

    # Embed in batches
    for i in range(0, len(all_chunks), batch_size):
        batch_texts = all_chunks[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        batch_meta = metadata_list[i:i+batch_size]

        embeddings = embed_texts(batch_texts)

        if not embeddings:
            print(f"⚠️ Skipping batch {i//batch_size + 1}, no embeddings returned")
            continue

        for vid, emb, meta in zip(batch_ids, embeddings, batch_meta):
            if emb:  # Ensure not None/empty
                records.append({
                    "id": vid,
                    "values": emb,
                    "metadata": meta
                })

        print(f"✅ Processed batch {i//batch_size + 1}, got {len(embeddings)} embeddings")

    print(f"📦 Total vectors prepared: {len(records)}")

    if not records:
        print("🚨 No vectors to upload. Check embedding quota or errors.")
        return

    # Upload in chunks
    print("📤 Uploading vectors to Pinecone...")
    for i in range(0, len(records), 100):
        index.upsert(vectors=records[i:i+100])
        print(f"   ⬆️ Uploaded {min(i+100, len(records))}/{len(records)} vectors")

    print(f"🎉 Ingested {len(records)} chunks into Pinecone.")


if __name__ == "__main__":
    ingest_dataset()
