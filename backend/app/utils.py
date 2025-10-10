import os
import uuid
import re
from PyPDF2 import PdfReader
from docx import Document

# -------------------------------
# 1️⃣ File Validation
# -------------------------------
def allowed_file(filename, allowed_extensions={"pdf", "txt", "docx"}):
    """
    Check if the uploaded file has an allowed extension.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


# -------------------------------
# 2️⃣ Unique ID Generator
# -------------------------------
def generate_id(prefix="doc"):
    """
    Generate a unique ID using UUID4.
    """
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


# -------------------------------
# 3️⃣ Text Extraction from Documents
# -------------------------------
def extract_text_from_file(filepath):
    """
    Extract text content from PDF, DOCX, or TXT files.
    """
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(filepath)
    elif ext == ".docx":
        return extract_text_from_docx(filepath)
    elif ext == ".txt":
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def extract_text_from_pdf(filepath):
    """
    Extracts text from a PDF file using PyPDF2.
    """
    text = ""
    try:
        reader = PdfReader(filepath)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"[ERROR] Failed to read PDF {filepath}: {e}")
    return text


def extract_text_from_docx(filepath):
    """
    Extracts text from a DOCX file using python-docx.
    """
    text = ""
    try:
        doc = Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"[ERROR] Failed to read DOCX {filepath}: {e}")
    return text


# -------------------------------
# 4️⃣ Text Cleaning
# -------------------------------
def clean_text(text):
    """
    Removes unnecessary spaces, symbols, and newlines.
    """
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


# -------------------------------
# 5️⃣ Text Chunking
# -------------------------------
def chunk_text(text, chunk_size=1000, overlap=100):
    """
    Split large text into chunks for embedding and retrieval.

    Args:
        text: the full extracted text
        chunk_size: number of characters per chunk
        overlap: number of overlapping characters between chunks
    Returns:
        list of text chunks
    """
    text = clean_text(text)
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


# -------------------------------
# 6️⃣ Logger
# -------------------------------
def log(message):
    """
    Simple logger for console.
    """
    print(f"[RAG] {message}")
