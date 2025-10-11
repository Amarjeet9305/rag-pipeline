# from flask import Flask
# from app.routes.upload import upload_bp
# from app.routes.query import query_bp
# from app.routes.metadata import metadata_bp

# def create_app():
#     app = Flask(__name__)

#     # Register blueprints
#     app.register_blueprint(upload_bp, url_prefix='/upload')
#     app.register_blueprint(query_bp, url_prefix='/query')
#     app.register_blueprint(metadata_bp, url_prefix='/metadata')

#     @app.route('/')
#     def index():
#         return "<h2>RAG Flask System Running 🚀</h2>"

#     return app

# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)
# from flask import Flask, render_template
# from app.routes.upload import upload_bp
# from app.routes.query import query_bp
# from app.routes.metadata import metadata_bp

# app = Flask(__name__)

# # Register blueprints
# app.register_blueprint(upload_bp)
# app.register_blueprint(query_bp)
# app.register_blueprint(metadata_bp)

# # Serve frontend
# @app.route("/")
# def index():
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000, debug=True)

# from flask import Flask, render_template
# from flask_cors import CORS  # ✅ Allow frontend requests (important!)
# from app.routes.upload import upload_bp
# from app.routes.query import query_bp
# from app.routes.metadata import metadata_bp

# # ✅ Create Flask app
# app = Flask(
#     __name__,
#     static_folder="../frontend/static",   # where styles.css and app.js are stored
#     template_folder="../frontend/templates"  # where index.html is stored
# )

# # ✅ Enable CORS so frontend (e.g. http://127.0.0.1:5500) can talk to Flask
# CORS(app)

# # ✅ Register blueprints
# app.register_blueprint(upload_bp)
# app.register_blueprint(query_bp)
# app.register_blueprint(metadata_bp)

# # ✅ Serve index.html (main UI)
# @app.route("/")
# def index():
#     return render_template("index.html")

# # ✅ Run Flask app
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=8000, debug=True)
# import os
# from flask import Flask, render_template
# from flask_cors import CORS
# from app.routes.upload import upload_bp
# from app.routes.query import query_bp
# from app.routes.metadata import metadata_bp

# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# app = Flask(
#     __name__,
#     static_folder=os.path.join(BASE_DIR, "frontend", "static"),
#     template_folder=os.path.join(BASE_DIR, "frontend", "templates")
# )

# # ✅ Enable CORS for all routes
# CORS(app, resources={r"/*": {"origins": "*"}})

# # ✅ Register blueprints with prefixes
# app.register_blueprint(upload_bp, url_prefix="/api")
# app.register_blueprint(query_bp, url_prefix="/api")
# app.register_blueprint(metadata_bp, url_prefix="/api")

# @app.route("/")
# def index():
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=8000, debug=True)
#     app.run(debug=True, use_reloader=False)
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from app.models import db_models  # your existing db_models.py
# import os

# app = Flask(__name__)
# CORS(app)  # Allow frontend on different port

# # Make uploads folder if not exists
# UPLOAD_FOLDER = "./uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# @app.route("/", methods=["GET"])
# def home():
#     return "Backend is running. Use /upload (POST) or /metadata (GET)."


# @app.route("/upload", methods=["POST"])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({"message": "No file part"}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"message": "No selected file"}), 400

#     # Save file
#     filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(filepath)

#     # Insert metadata into MongoDB
#     doc_id = file.filename.split('.')[0]
#     db_models.insert_document_metadata(
#         filename=file.filename,
#         filepath=filepath,
#         num_chunks=0,
#         file_size=os.path.getsize(filepath),
#         doc_id=doc_id
#     )

#     return jsonify({"message": "File uploaded successfully"}), 200


# @app.route("/metadata", methods=["GET"])
# def get_metadata():
#     docs = db_models.get_all_doc()
#     return jsonify(docs), 200


# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=8000, debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from app.models import db_models  # your existing db_models.py
import os

app = Flask(__name__)
CORS(app)  # Allow frontend (React/HTML/JS) to communicate

# Directory for file uploads
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- Home Route ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "✅ Backend is running.",
        "routes": ["/upload (POST)", "/metadata (GET)", "/ask (POST)"]
    }), 200


# ---------------- File Upload ----------------
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "❌ No file found in request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "❌ No file selected"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Save metadata to DB (Mongo, etc.)
    doc_id = file.filename.split(".")[0]
    db_models.insert_document_metadata(
        filename=file.filename,
        filepath=filepath,
        num_chunks=0,
        file_size=os.path.getsize(filepath),
        doc_id=doc_id
    )

    return jsonify({"message": "✅ File uploaded successfully", "filename": file.filename}), 200


# ---------------- Get Metadata ----------------
@app.route("/metadata", methods=["GET"])
def get_metadata():
    try:
        docs = db_models.get_all_doc()
        if not docs:
            return jsonify({"message": "No documents found", "data": []}), 200
        return jsonify(docs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- Chat Ask Endpoint ----------------
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"error": "Missing 'question' in request body"}), 400

        user_q = data["question"]

        # 🧠 Placeholder: Replace with your RAG / LLM pipeline
        answer = f"You asked: '{user_q}'. I’ll process this with document context soon."

        return jsonify({"answer": answer}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- Run Server ----------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)

