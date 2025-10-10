# backend/app/services/rag.py

from app.services.vector_store import query_vector_db
from app.services.embeddings import create_embeddings, generate_answer
from app.utils import log, clean_text


def answer_query(query_text, doc_ids=None, top_k=5):
    """
    Retrieve top-k most relevant document chunks and generate an LLM-based answer.

    Args:
        query_text (str): User query.
        doc_ids (list[str], optional): Specific document IDs to filter results.
        top_k (int): Number of top chunks to retrieve from vector DB.

    Returns:
        tuple: (answer_text, retrieved_metadata)
    """
    log(f"Received query: {query_text}")

    # Step 1: Embed the query
    query_embedding = create_embeddings([query_text])[0]

    # Step 2: Retrieve top-k chunks from Chroma vector store
    results = query_vector_db(query_embedding, top_k=top_k)
    retrieved_texts = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not retrieved_texts:
        log("No relevant chunks found for the query.")
        return "No relevant information found.", []

    # Step 3: Optional filtering by specific doc_ids
    if doc_ids:
        filtered_pairs = [
            (t, m) for t, m in zip(retrieved_texts, metadatas)
            if m.get("doc_id") in doc_ids
        ]
        if filtered_pairs:
            retrieved_texts, metadatas = zip(*filtered_pairs)
        else:
            # If no chunks match doc_ids, keep original
            retrieved_texts, metadatas = retrieved_texts, metadatas

    # Step 4: Prepare context for the LLM
    context = "\n\n".join(retrieved_texts)
    prompt = f"""
You are an intelligent assistant. Use the following context to answer the user's query concisely.

Context:
{context}

Question:
{query_text}

Answer:"""

    # Step 5: Generate answer using Groq API
    answer = generate_answer(prompt)
    answer = clean_text(answer)

    log("Generated LLM answer successfully.")
    return answer, metadatas
