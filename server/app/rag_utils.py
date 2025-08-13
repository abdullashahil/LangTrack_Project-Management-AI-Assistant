def chunk_text(text, max_chars=1200, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks

def build_prompt(question, contexts):
    ctx_str = "\n\n".join([f"[{i+1}] {c}" for i, c in enumerate(contexts)])
    return f"""
You are a helpful assistant. Use only this context to answer:

{ctx_str}

Question: {question}
"""
