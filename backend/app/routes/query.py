# backend/app/routes/query.py
from flask import Blueprint, request, jsonify
from app.services.rag import answer_query  # Only import the correct function

query_bp = Blueprint("query", __name__)

@query_bp.route("/query", methods=["POST"])
def query():
    data = request.json
    if not data or "query" not in data:
        return jsonify({"error": "Query text is required"}), 400

    query_text = data["query"]
    doc_ids = data.get("doc_ids")  # Optional filter by document IDs
    k = data.get("k", 5)           # Optional: number of chunks to retrieve

    # Call the RAG pipeline
    answer, provenance = answer_query(query_text, doc_ids=doc_ids, k=k)

    return jsonify({
        "query": query_text,
        "answer": answer,
        "provenance": provenance
    }), 200
