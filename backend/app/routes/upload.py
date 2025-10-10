from flask import Blueprint, request, jsonify
from app.services.ingest import process_and_store_file  # <-- FIXED import

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/", methods=["POST"])  # endpoint will be /upload/ when registered
def upload():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files uploaded"}), 400
    if len(files) > 20:
        return jsonify({"error": "Maximum 20 files allowed"}), 400

    results = []
    for f in files:
        res = process_and_store_file(f)
        results.append(res)

    return jsonify({"uploaded": results}), 200
