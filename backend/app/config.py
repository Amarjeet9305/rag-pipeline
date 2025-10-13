# backend/app/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if exists)
load_dotenv()

# -----------------------------
# Groq API
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set! Please set it in your environment or .env file.")

# -----------------------------
# MongoDB config
# -----------------------------
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/ragdb")
DB_NAME = "ragdb"

# -----------------------------
# Chroma Vector DB
# -----------------------------
VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", "./vector_db")

# -----------------------------
# Flask Upload Settings
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max per file
ALLOWED_EXTENSIONS = {"pdf", "txt", "docx"}
print("✅ GROQ_API_KEY loaded:", bool(GROQ_API_KEY))

