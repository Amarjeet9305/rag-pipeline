# RAG Pipeline Chat - Backend





---

## Features

- Upload documents via `/upload` endpoint
- Store document metadata in a database
- Process documents into chunks and generate embeddings
- Query uploaded documents with `/query` endpoint using RAG
- Retrieve uploaded document metadata via `/metadata` endpoint
- CORS enabled for frontend communication

---

## Tech Stack

- **Backend:** Python, Flask
- **Vector Store:** Chroma (or custom vector store)
- **AI API:** Groq API
- **Frontend:** HTML/JS (integrated separately)
- **File Handling:** Local `uploads` directory

---

## Setup & Installation

1. **Clone the repository**

```bash
git clone <repo-url>
cd rag-pipeline/backend
