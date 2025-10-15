# # backend/app/main.py
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from app.models import db_models  # your existing db_models.py
# from app.config import GROQ_API_KEY
# import os
# # Import Blueprints
# from app.routes.upload import upload_bp
# from app.routes.query import query_bp
# from app.routes.metadata import metadata_bp

# app = Flask(__name__)
# CORS(app)  # Allow frontend to communicate
# # ---------------- Register Blueprints ----------------
# app.register_blueprint(upload_bp, url_prefix="/upload") 
# app.register_blueprint(query_bp) # query.py will handle /query
# app.register_blueprint(metadata_bp) # metadata.py will handle /metadata

# # Directory for file uploads
# UPLOAD_FOLDER = "./uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # ---------------- Home Route ----------------
# @app.route("/", methods=["GET"])
# def home():
#     return jsonify({
#         "message": "✅ Backend is running.",
#         "routes": ["/upload (POST)", "/metadata (GET)", "/ask (POST)", "/query (POST)"]
#     }), 200

# # ---------------- File Upload ----------------
# @app.route("/upload", methods=["POST"])
# def upload_file():
#     if "file" not in request.files:
#         return jsonify({"message": "❌ No file found in request"}), 400

#     file = request.files["file"]
#     if file.filename == "":
#         return jsonify({"message": "❌ No file selected"}), 400

#     filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(filepath)

#     # Save metadata to DB
#     doc_id = file.filename.split(".")[0]
#     db_models.insert_document_metadata(
#         filename=file.filename,
#         filepath=filepath,
#         num_chunks=0,
#         file_size=os.path.getsize(filepath),
#         doc_id=doc_id
#     )

#     return jsonify({"message": "✅ File uploaded successfully", "filename": file.filename}), 200

# # ---------------- Get Metadata ----------------
# @app.route("/metadata", methods=["GET"])
# def get_metadata():
#     try:
#         docs = db_models.get_all_doc()
#         if not docs:
#             return jsonify({"message": "No documents found", "data": []}), 200
#         return jsonify(docs), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # ---------------- Chat Ask Endpoint ----------------
# @app.route("/ask", methods=["POST"])
# def ask():
#     try:
#         data = request.get_json()
#         if not data or "question" not in data:
#             return jsonify({"error": "Missing 'question' in request body"}), 400

#         user_q = data["question"]

#         # 🧠 Placeholder: Replace with your RAG / LLM pipeline
#         answer = f"You asked: '{user_q}'. I’ll process this with document context soon."

#         return jsonify({"answer": answer}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # ---------------- GROQ Query Endpoint ----------------
# @app.route("/query", methods=["POST"])
# def query_doc():
#     data = request.get_json()
#     query = data.get("query", "")

#     if not query:
#         return jsonify({"error": "No query provided"}), 400

#     # 🔹 Integrate your GROQ API here
#     # For now, simulate a response
#     simulated_answer = f"✅ GROQ API working! You asked: '{query}'. This would return a real AI-generated answer."
#     return jsonify({"answer": simulated_answer})

# # ---------------- Run Server ----------------
# if __name__ == "__main__":
#     print(f"✅ GROQ_API_KEY loaded: {bool(GROQ_API_KEY)}")
#     app.run(host="127.0.0.1", port=8000, debug=True)
# app/main.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from app.models import db_models  # your existing db_models.py
from app.config import GROQ_API_KEY
import os

# Import Blueprints
from app.routes.upload import upload_bp
from app.routes.query import query_bp
from app.routes.metadata import metadata_bp

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate

# Directory for file uploads
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- Register Blueprints ----------------
# FIX: Set strict_slashes=False to resolve the 308 Permanent Redirect error.
# This allows access to /query and /query/ (and /upload, /metadata)
app.register_blueprint(upload_bp, url_prefix="/upload", strict_slashes=False) 
app.register_blueprint(query_bp, url_prefix="/query", strict_slashes=False)
app.register_blueprint(metadata_bp, url_prefix="/metadata", strict_slashes=False) 

# ---------------- Home Route ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "✅ Backend is running.",
        "routes": ["/upload (POST)", "/metadata (GET)", "/query (POST)"] # Removed /ask for cleaner structure
    }), 200

# ---------------- File Upload (Legacy/Root Handlers) ----------------
# NOTE: These routes are redundant if the Blueprints handle them, 
# but are kept here to match the structure of the file you provided.
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "❌ No file found in request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "❌ No file selected"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Save metadata to DB
    doc_id = file.filename.split(".")[0]
    db_models.insert_document_metadata(
        filename=file.filename,
        filepath=filepath,
        num_chunks=0,
        file_size=os.path.getsize(filepath),
        doc_id=doc_id
    )

    return jsonify({"message": "✅ File uploaded successfully", "filename": file.filename}), 200

@app.route("/metadata", methods=["GET"])
def get_metadata():
    try:
        docs = db_models.get_all_doc()
        if not docs:
            return jsonify({"message": "No documents found", "data": []}), 200
        return jsonify(docs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- Run Server ----------------
if __name__ == "__main__":
    print(f"✅ GROQ_API_KEY loaded: {bool(GROQ_API_KEY)}")
    # Changed host to 0.0.0.0 for better compatibility, consistent with your logs.
    app.run(host="0.0.0.0", port=8000, debug=True)
