import chromadb
from chromadb.utils import embedding_functions
import app.config as config
from app.utils import log
import requests
import os

# Initialize Chroma client
chroma_client = chromadb.Client()

# Get or create a collection for storing document chunks
collection = chroma_client.get_or_create_collection(name="rag_collection")

# --- Embedding Helper ---

def get_text_embedding(text):
    """
    Get text embedding using Groq API.
    """
    try:
        GROQ_API_KEY = os.getenv("GROQ_API_KEY", config.GROQ_API_KEY)
        if not GROQ_API_KEY:
            raise ValueError("Missing GROQ_API_KEY")

        url = "https://api.groq.com/openai/v1/embeddings"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "input": text,
            "model": "nomic-embed-text-v1.5"  # "text-embedding-ada-002" Replace with Groq-supported embedding model if different
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        embedding = response.json()["data"][0]["embedding"]
        return embedding
    except Exception as e:
        log(f"Error generating embedding: {e}")
        return None

# --- Add embeddings to DB ---

def add_embeddings(chunks, embeddings):
    """
    Add document chunks and their embeddings to Chroma collection.
    """
    try:
        for chunk, emb in zip(chunks, embeddings):
            collection.add(
                documents=[chunk["text"]],
                metadatas=[{"doc_id": chunk["doc_id"], "chunk_id": chunk["chunk_id"]}],
                embeddings=[emb]
            )
        log(f" Added {len(chunks)} chunks to vector store.")
    except Exception as e:
        log(f" Error adding embeddings: {e}")

# --- Query embeddings from DB ---

def query_vector_db(query_embedding, top_k=5):
    """
    Query Chroma DB with query embedding to retrieve top-k similar chunks.
    """
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        log(f"🔍 Retrieved {len(results.get('documents', [[]])[0])} chunks from vector store.")
        return results
    except Exception as e:
        log(f" Error querying vector DB: {e}")
        return {"documents": [[]], "metadatas": [[]]}

# --- Search helper (used by /query route) ---

def search_embeddings(query_text, top_k=5):
    """
    High-level search function:
    1. Generate embedding for user query.
    2. Query vector database for top matches.
    """
    query_embedding = get_text_embedding(query_text)
    if query_embedding is None:
        log(" Failed to get query embedding.")
        return {"documents": [[]], "metadatas": [[]]}

    results = query_vector_db(query_embedding, top_k=top_k)
    return results

