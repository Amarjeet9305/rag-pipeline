# backend/app/services/ingest.py
import os
from datetime import datetime
from werkzeug.utils import secure_filename

# Absolute imports from your app package
from app.utils import (
    allowed_file,
    extract_text_from_file,
    chunk_text,
    generate_id,
    log
)
from app.services.embeddings import create_embeddings
from app.services.vector_store import add_embeddings
from app.models.db_models import insert_document_metadata, insert_chunk_metadata
import app.config as config


def process_and_store_file(file_path):
    """
    Process an uploaded file:
    1. Extract text
    2. Chunk text
    3. Generate embeddings
    4. Store embeddings in Chroma/FAISS
    5. Save document and chunk metadata in MongoDB
    """

    filename = os.path.basename(file_path)
    filename = secure_filename(filename)

    # Check allowed file types
    if not allowed_file(filename):
        log(f" File type not allowed: {filename}")
        return {"error": f"File type not allowed: {filename}"}

    # Verify file exists
    if not os.path.exists(file_path):
        log(f" File does not exist: {file_path}")
        return {"error": f"File not found: {file_path}"}

    file_size = os.path.getsize(file_path)

    # Generate a unique document ID
    doc_id = generate_id("doc")
    log(f"📄 Processing document: {filename} (ID: {doc_id})")

    # Step 1: Extract text from file
    try:
        text = extract_text_from_file(file_path)
        if not text.strip():
            log(f"⚠️ No text extracted from {filename}")
            return {"error": f"No text could be extracted from {filename}"}
    except Exception as e:
        log(f" Text extraction failed for {filename}: {e}")
        return {"error": f"Text extraction failed for {filename}: {e}"}

    # Step 2: Chunk the text
    chunks = chunk_text(text, chunk_size=1000, overlap=100)
    log(f" Generated {len(chunks)} chunks from {filename}")

    #  Step 3: Generate embeddings for chunks
    try:
        embeddings = create_embeddings(chunks)
        log(f" Created embeddings for {filename}")
    except Exception as e:
        log(f" Embedding creation failed for {filename}: {e}")
        return {"error": f"Embedding creation failed for {filename}: {e}"}

    # Step 4: Store embeddings in vector store
    chunk_data = []
    for i, chunk_text_data in enumerate(chunks):
        chunk_id = generate_id("chunk")
        chunk_data.append({
            "text": chunk_text_data,
            "chunk_id": chunk_id,
            "doc_id": doc_id
        })

    try:
        add_embeddings(chunk_data, embeddings)
        log(f" Stored embeddings for {filename}")
    except Exception as e:
        log(f" Failed to store embeddings for {filename}: {e}")
        return {"error": f"Failed to store embeddings for {filename}: {e}"}

    # Step 5: Store metadata in MongoDB
    try:
        insert_document_metadata(filename, file_path, len(chunks), file_size, doc_id)
        for c in chunk_data:
            insert_chunk_metadata(c["doc_id"], c["chunk_id"], c["text"])
        log(f" Stored metadata for {filename}")
    except Exception as e:
        log(f" Failed to store metadata for {filename}: {e}")
        return {"error": f"Failed to store metadata for {filename}: {e}"}

    log(f" Document {filename} successfully processed and stored.")

    return {
        "filename": filename,
        "doc_id": doc_id,
        "chunks": len(chunks),
        "status": "success"
    }
