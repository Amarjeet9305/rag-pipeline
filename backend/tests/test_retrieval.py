import pytest
from rag import retrieve_relevant_chunks, generate_response

@pytest.fixture
def mock_docs():
    return ["AI improves productivity.", "AI powers automation."]

def test_retrieve_relevant_chunks(mock_docs):
    query = "How does AI help in automation?"
    results = retrieve_relevant_chunks(query, mock_docs)
    assert isinstance(results, list)
    assert all(isinstance(r, str) for r in results)

def test_generate_response(monkeypatch):
    def mock_api_call(prompt):
        return "AI helps automation through machine learning."
    monkeypatch.setattr("rag.call_llm_api", mock_api_call)

    context = ["AI powers automation."]
    query = "Explain how AI automates tasks."
    response = generate_response(query, context)
    assert "AI" in response
