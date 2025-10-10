# backend/app/services/vector_store.py

import chromadb
from chromadb.utils import embedding_functions
import app.config as config
from app.utils import log

# Initialize Chroma client
chroma_client = chromadb.Client()

# Get or create a collection for storing document chunks
collection = chroma_client.get_or_create_collection(
    name="rag_collection"
)

def add_embeddings(chunks, embeddings):
    """
    Add document chunks and their embeddings to Chroma collection.

    Args:
        chunks (list[dict]): List of chunk dictionaries with 'text', 'doc_id', 'chunk_id'.
        embeddings (list[list[float]]): List of corresponding embeddings.
    """
    try:
        for chunk, emb in zip(chunks, embeddings):
            collection.add(
                documents=[chunk["text"]],
                metadatas=[{"doc_id": chunk["doc_id"], "chunk_id": chunk["chunk_id"]}],
                embeddings=[emb]
            )
        log(f"Added {len(chunks)} chunks to vector store.")
    except Exception as e:
        log(f"Error adding embeddings: {e}")


def query_vector_db(query_embedding, top_k=5):
    """
    Query the Chroma vector database to retrieve top-k most similar chunks.

    Args:
        query_embedding (list[float]): Embedding of the query text.
        top_k (int): Number of top results to return.

    Returns:
        dict: Dictionary containing 'documents' and 'metadatas'.
    """
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        log(f"Retrieved {len(results.get('documents', [[]])[0])} chunks from vector store.")
        return results
    except Exception as e:
        log(f"Error querying vector DB: {e}")
        return {"documents": [[]], "metadatas": [[]]}
