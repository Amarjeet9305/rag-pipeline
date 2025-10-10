# backend/app/models/db_models.py
import app.config as config  # Absolute import
from pymongo import MongoClient
from datetime import datetime

# MongoDB client
client = MongoClient(config.MONGO_URI)
db = client[config.DB_NAME]

# Collections
documents_collection = db.documents
chunks_collection = db.chunks

def insert_document_metadata(filename, filepath, num_chunks, file_size, doc_id):
    """
    Insert document metadata into MongoDB.
    """
    doc = {
        "doc_id": doc_id,
        "filename": filename,
        "filepath": filepath,
        "num_chunks": num_chunks,
        "file_size": file_size,
        "created_at": datetime.utcnow()
    }
    documents_collection.insert_one(doc)

def insert_chunk_metadata(doc_id, chunk_id, text):
    """
    Insert a chunk's metadata into MongoDB.
    """
    chunk = {
        "chunk_id": chunk_id,
        "doc_id": doc_id,
        "text": text,
        "created_at": datetime.utcnow()
    }
    chunks_collection.insert_one(chunk)

def get_all_doc():
    """
    Retrieve all document metadata from MongoDB.
    Returns:
        List of document dictionaries (without MongoDB _id)
    """
    docs = list(documents_collection.find({}, {"_id": 0}))
    return docs
