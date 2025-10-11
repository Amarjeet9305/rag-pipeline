# from flask import Blueprint, request, jsonify
# from app.services.vector_store import search_embeddings
# from app.config import GROQ_API_KEY
# import requests
# import json

# query_bp = Blueprint("query", __name__, url_prefix="/query")

# # Groq model setup (using llama3 or mixtral)
# GROQ_MODEL = "llama3-70b-8192"  # or "mixtral-8x7b-32768"
# GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


# @query_bp.route("/", methods=["POST"])
# def query():
#     try:
#         data = request.get_json()
#         user_query = data.get("query", "").strip()

#         if not user_query:
#             return jsonify({"error": "No query provided"}), 400

#         # ✅ Retrieve top relevant chunks from vector store
#         relevant_docs = search_embeddings(user_query, top_k=3)
#         context = "\n\n".join([doc["text"] for doc in relevant_docs]) if relevant_docs else ""

#         if not context:
#             return jsonify({
#                 "answer": "No relevant document found. Please upload a file first."
#             })

#         # ✅ Construct Groq API payload
#         headers = {
#             "Authorization": f"Bearer {GROQ_API_KEY}",
#             "Content-Type": "application/json",
#         }

#         payload = {
#             "model": GROQ_MODEL,
#             "messages": [
#                 {"role": "system", "content": "You are a helpful assistant that answers based on provided context."},
#                 {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{user_query}"}
#             ],
#             "temperature": 0.3,
#             "max_tokens": 500
#         }

#         # Call Groq API
#         response = requests.post(GROQ_URL, headers=headers, data=json.dumps(payload))
#         response.raise_for_status()
#         result = response.json()

#         #  Extract answer
#         answer = result["choices"][0]["message"]["content"]

#         return jsonify({
#             "answer": answer,
#             "context_used": len(relevant_docs)
#         })

#     except Exception as e:
#         print(f" Query error: {e}")
#         return jsonify({"error": f"Query processing failed: {str(e)}"}), 500

from flask import Blueprint, request, jsonify
from app.services.vector_store import search_embeddings
from app.config import GROQ_API_KEY
import requests
import json

query_bp = Blueprint("query", __name__, url_prefix="/query")

# ✅ Available Groq models
AVAILABLE_MODELS = {
    "llama3": "llama3-70b-8192",
    "mixtral": "mixtral-8x7b-32768",
    "gemma2": "gemma2-9b-it"
}

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


@query_bp.route("/", methods=["POST"])
def query():
    try:
        data = request.get_json()
        user_query = data.get("query", "").strip()
        model_key = data.get("model", "llama3").lower()  # default to llama3

        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        # ✅ Validate selected model
        if model_key not in AVAILABLE_MODELS:
            return jsonify({
                "error": f"Invalid model '{model_key}'. Available models: {list(AVAILABLE_MODELS.keys())}"
            }), 400

        selected_model = AVAILABLE_MODELS[model_key]
        print(f"🧠 Using model: {selected_model}")

        # ✅ Retrieve top relevant chunks from vector store
        relevant_docs = search_embeddings(user_query, top_k=3)
        context = "\n\n".join([doc["text"] for doc in relevant_docs]) if relevant_docs else ""

        if not context:
            return jsonify({
                "answer": "No relevant document found. Please upload a file first."
            })

        # ✅ Construct Groq API payload
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": selected_model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that answers based on provided context."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{user_query}"}
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }

        # ✅ Call Groq API
        response = requests.post(GROQ_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()

        # ✅ Extract answer
        answer = result["choices"][0]["message"]["content"]

        print(f"✅ Query successful | Model: {selected_model} | Contexts used: {len(relevant_docs)}")

        return jsonify({
            "answer": answer,
            "model_used": selected_model,
            "context_used": len(relevant_docs)
        })

    except Exception as e:
        print(f"❌ Query error: {e}")
        return jsonify({"error": f"Query processing failed: {str(e)}"}), 500
