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
    
    # One-shot example
    example = """
Example:
Context:
[1] Project ID: P001 | Project Name: Renovation of a School Project 001 | Project Type: Renovation | Location: Texas | Start Date: 21/07/2024 | End Date: 08/08/2024 | Status: Behind Schedule

Question: What is the location of Project P001?
Answer: The location of Project P001 is Texas.
"""

    return f"""
You are a helpful assistant. Use only the provided context to answer questions about the projects.  
If the question is a greeting (like "hi", "hello") or unrelated to the context, reply politely without requiring the context.

{ctx_str}

{example}

Now, answer the following question based on the given context:

Question: {question}
Answer:
"""
