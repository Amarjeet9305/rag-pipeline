from flask import Blueprint, request, jsonify
from app.services.vector_store import search_embeddings
from app.config import GROQ_API_KEY
import requests
import json

query_bp = Blueprint("query", __name__, url_prefix="/query")

# Multiple model options
GROQ_MODELS = {
    "llama3-8b": "llama3-8b-8192",
    "llama3-70b": "llama3-70b-8192",
    "mixtral": "mixtral-8x7b-32768"
}

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@query_bp.route("/", methods=["POST"])
def query():
    try:
        data = request.get_json()
        user_query = data.get("query", "").strip()
        model_choice = data.get("model", "llama3-8b")

        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        # ✅ Retrieve top relevant chunks from vector store
        relevant_docs = search_embeddings(user_query, top_k=3)
        context = "\n\n".join([doc["text"] for doc in relevant_docs]) if relevant_docs else ""

        if not context:
            return jsonify({
                "answer": "⚠️ No relevant content found. Please upload a document first."
            })

        # ✅ Construct Groq API payload
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": GROQ_MODELS.get(model_choice, "llama3-8b-8192"),
            "messages": [
                {"role": "system", "content": "You are an assistant that answers based on the document context."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{user_query}"}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }

        print(f"\n🚀 Sending request to Groq model: {payload['model']}")
        response = requests.post(GROQ_URL, headers=headers, data=json.dumps(payload))
        print("📩 Groq Status:", response.status_code)

        if response.status_code != 200:
            print("❌ Groq API Error:", response.text)
            return jsonify({"error": "Groq API request failed", "details": response.text}), 500

        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        print("✅ Groq Response:", answer[:200], "...")
        return jsonify({
            "answer": answer,
            "context_used": len(relevant_docs),
            "model_used": payload["model"]
        })

    except Exception as e:
        print(f"❌ Query error: {e}")
        return jsonify({"error": f"Query failed: {str(e)}"}), 500

