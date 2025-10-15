# from flask import Blueprint, request, jsonify
# from app.services.vector_store import search_embeddings
# from app.config import GROQ_API_KEY
# import requests
# import json
# from app.utils import log 

# # FIX 1: Ensure the blueprint is created without a local url_prefix
# # This is correct and adheres to the requested permanent fix.
# query_bp = Blueprint("query", __name__) 

# # Multiple model options
# GROQ_MODELS = {
#     "llama3-8b": "llama3-8b-8192",
#     "llama3-70b": "llama3-70b-8192",
#     "mixtral": "mixtral-8x7b-32768"
# }

# GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# # FIX 2: Explicitly define the route as both / and without trailing slash, 
# # although the main.py fix should handle this. We add the explicit definition just in case.
# # Note: Since strict_slashes=False is set in main.py, we only need to define one of them.
# # The route is relative to the url_prefix defined in main.py (e.g., /query/)
# @query_bp.route("/", methods=["POST"]) 
# def query():
#     try:
#         data = request.get_json()
#         user_query = data.get("query", "").strip()
#         model_choice = data.get("model", "llama3-8b")

#         if not user_query:
#             return jsonify({"error": "No query provided"}), 400

#         # ✅ Retrieve top relevant chunks from vector store
#         relevant_docs = search_embeddings(user_query, top_k=3)
        
#         # NOTE: Using "documents" key as per vector_store.py results structure
#         if relevant_docs and relevant_docs.get("documents", [[]]) and relevant_docs["documents"][0]:
#             context = "\n\n".join(relevant_docs["documents"][0])
#         else:
#             context = ""
            
#         if not context:
#             return jsonify({
#                 "answer": "⚠️ No relevant content found. Please upload a document first."
#             })

#         # ✅ Construct Groq API payload
#         headers = {
#             "Authorization": f"Bearer {GROQ_API_KEY}",
#             "Content-Type": "application/json",
#         }

#         payload = {
#             "model": GROQ_MODELS.get(model_choice, "llama3-8b-8192"),
#             "messages": [
#                 {"role": "system", "content": "You are an assistant that answers based on the document context. If you cannot find an answer in the context, politely state that you do not have enough information."},
#                 {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{user_query}"}
#             ],
#             "temperature": 0.3,
#             "max_tokens": 1000
#         }

#         # Use log() instead of print() if utils.py defines it
#         log(f"\n🚀 Sending request to Groq model: {payload['model']}")
#         response = requests.post(GROQ_URL, headers=headers, data=json.dumps(payload))
#         log(f"📩 Groq Status: {response.status_code}")

#         # ✅ Handle non-200 responses safely
#         if response.status_code != 200:
#             log(f"❌ Groq API Error: {response.text}")
#             return jsonify({
#                 "answer": "Groq API request failed.",
#                 "details": response.text
#             }), 500

#         # ✅ Parse response JSON safely
#         try:
#             result = response.json()
#         except Exception as e:
#             log(f"❌ Invalid JSON from Groq: {e}")
#             return jsonify({
#                 "answer": "Groq returned invalid JSON response.",
#                 "details": str(e)
#             }), 500

#         # ⚠️ Check for model response
#         if not result.get("choices") or not result["choices"][0].get("message"):
#             log(f"❌ Groq Response Lacks Choices/Message: {result}")
#             return jsonify({
#                 "answer": "Groq returned an empty response or an unexpected structure.",
#                 "details": result.get("error", "No error details provided.")
#             }), 500

#         # ✅ Safe parsing of the content
#         answer = result["choices"][0]["message"].get("content", "No content provided by Groq model.")

#         log(f"✅ Groq Response: {answer[:200]} ...")
#         return jsonify({
#             "answer": answer,
#             "context_used": len(relevant_docs["documents"][0]),
#             "model_used": payload["model"]
#         })

#     except Exception as e:
#         log(f"❌ Query error: {e}")
#         return jsonify({"answer": f"A critical backend error occurred: {str(e)}"}), 500

# app/routes/query.py
from flask import Blueprint, request, jsonify
from app.services.vector_store import search_embeddings
from app.config import GROQ_API_KEY
import requests
import json
from app.utils import log 

# FIX 1: Ensure the blueprint is created without a local url_prefix.
# The prefix is handled by main.py.
query_bp = Blueprint("query", __name__) 

# Multiple model options
GROQ_MODELS = {
    "llama3-8b": "llama3-8b-8192",
    "llama3-70b": "llama3-70b-8192",
    "mixtral": "mixtral-8x7b-32768"
}

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# FIX 2: Define the route as "/", which, combined with the prefix "/query" 
# in main.py, creates the route /query/. The strict_slashes=False in main.py 
# ensures /query also works.
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
        
        # NOTE: Using "documents" key as per vector_store.py results structure
        if relevant_docs and relevant_docs.get("documents", [[]]) and relevant_docs["documents"][0]:
            context = "\n\n".join(relevant_docs["documents"][0])
        else:
            context = ""
            
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
                {"role": "system", "content": "You are an assistant that answers based on the document context. If you cannot find an answer in the context, politely state that you do not have enough information."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{user_query}"}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }

        # Use log() instead of print() if utils.py defines it
        log(f"\n🚀 Sending request to Groq model: {payload['model']}")
        response = requests.post(GROQ_URL, headers=headers, data=json.dumps(payload))
        log(f"📩 Groq Status: {response.status_code}")

        # ✅ Handle non-200 responses safely
        if response.status_code != 200:
            log(f"❌ Groq API Error: {response.text}")
            return jsonify({
                "answer": "Groq API request failed.",
                "details": response.text
            }), 500

        # ✅ Parse response JSON safely
        try:
            result = response.json()
        except Exception as e:
            log(f"❌ Invalid JSON from Groq: {e}")
            return jsonify({
                "answer": "Groq returned invalid JSON response.",
                "details": str(e)
            }), 500

        # ⚠️ Check for model response
        if not result.get("choices") or not result["choices"][0].get("message"):
            log(f"❌ Groq Response Lacks Choices/Message: {result}")
            return jsonify({
                "answer": "Groq returned an empty response or an unexpected structure.",
                "details": result.get("error", "No error details provided.")
            }), 500

        # ✅ Safe parsing of the content
        answer = result["choices"][0]["message"].get("content", "No content provided by Groq model.")

        log(f"✅ Groq Response: {answer[:200]} ...")
        return jsonify({
            "answer": answer,
            "context_used": len(relevant_docs["documents"][0]),
            "model_used": payload["model"]
        })

    except Exception as e:
        log(f"❌ Query error: {e}")
        return jsonify({"answer": f"A critical backend error occurred: {str(e)}"}), 500