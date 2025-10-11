from flask import Blueprint, request, jsonify
import os
from app.services.ingest import process_and_store_file

upload_bp = Blueprint("upload", __name__)

# Ensure upload folder exists
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@upload_bp.route("/", methods=["POST"])
def upload():
    try:
        files = request.files.getlist("files")

        if not files:
            return jsonify({"error": "No files uploaded"}), 400

        if len(files) > 20:
            return jsonify({"error": "Maximum 20 files allowed"}), 400

        results = []

        for f in files:
            # Save each file to disk
            file_path = os.path.join(UPLOAD_DIR, f.filename)
            f.save(file_path)

            print(f"📂 File saved: {file_path}")  # Debug log
            print("🚀 Calling process_and_store_file...")

            # Call ingestion
            try:
                res = process_and_store_file(file_path)
                print(f"✅ Ingestion completed for: {f.filename}")
                results.append({"file": f.filename, "status": "success"})
            except Exception as e:
                print(f"❌ Error ingesting {f.filename}: {e}")
                results.append({"file": f.filename, "status": "failed", "error": str(e)})

        return jsonify({"uploaded": results}), 200

    except Exception as e:
        print(f"🔥 Upload route error: {e}")
        return jsonify({"error": str(e)}), 500
