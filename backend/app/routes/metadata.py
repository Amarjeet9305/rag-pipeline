# backend/app/routes/metadata.py
from flask import Blueprint, jsonify
from app.models.db_models import get_all_doc  # <-- fixed absolute import

metadata_bp = Blueprint("metadata", __name__)

@metadata_bp.route("/metadata", methods=["GET"])
def metadata():
    docs = get_all_doc()  # fetch all document metadata
    return jsonify({"documents": docs}), 200
