import os
import pytest
from ingest import process_document, store_embeddings
from utils import get_vector_store

@pytest.fixture
def sample_text():
    return "Artificial intelligence is transforming industries."

def test_process_document(sample_text):
    chunks = process_document(sample_text)
    assert isinstance(chunks, list)
    assert all(isinstance(chunk, str) for chunk in chunks)
    assert len(chunks) > 0

def test_store_embeddings(tmp_path):
    vector_store = get_vector_store(os.path.join(tmp_path, "test_faiss"))
    embeddings = [[0.1, 0.2, 0.3]]
    store_embeddings(vector_store, embeddings, ["AI is the future."])
    assert len(vector_store.index_to_docstore_id) > 0
