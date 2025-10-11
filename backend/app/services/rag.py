# import os
# import requests
# from app.services.vector_store import query_vector_db
# from app.services.embeddings import create_embeddings
# from app.utils import log, clean_text
# import app.config as config


# def answer_query(query_text, doc_ids=None, top_k=5):
#     """
#     Retrieve top-k most relevant document chunks and generate an LLM-based answer using Groq API.

#     Args:
#         query_text (str): User query.
#         doc_ids (list[str], optional): Specific document IDs to filter results.
#         top_k (int): Number of top chunks to retrieve from vector DB.

#     Returns:
#         tuple: (answer_text, retrieved_metadata)
#     """
#     log(f"🧠 Received query: {query_text}")

#     # Step 1️⃣: Embed the query
#     try:
#         query_embedding = create_embeddings([query_text])[0]
#     except Exception as e:
#         log(f"❌ Error creating query embedding: {e}")
#         return f"Error creating embedding: {e}", []

#     # Step 2️⃣: Retrieve top-k chunks from Chroma vector store
#     try:
#         results = query_vector_db(query_embedding, top_k=top_k)
#         retrieved_texts = results.get("documents", [[]])[0]
#         metadatas = results.get("metadatas", [[]])[0]
#     except Exception as e:
#         log(f"❌ Error querying vector DB: {e}")
#         return f"Error querying vector DB: {e}", []

#     if not retrieved_texts:
#         log("⚠️ No relevant chunks found for the query.")
#         return "No relevant information found in uploaded documents.", []

#     # Step 3️⃣: Optional filtering by document IDs
#     if doc_ids:
#         filtered_pairs = [
#             (t, m) for t, m in zip(retrieved_texts, metadatas)
#             if m.get("doc_id") in doc_ids
#         ]
#         if filtered_pairs:
#             retrieved_texts, metadatas = zip(*filtered_pairs)
#         else:
#             log("⚠️ No chunks matched the provided doc_ids.")
#             retrieved_texts, metadatas = retrieved_texts, metadatas

#     # Step 4️⃣: Build the context prompt
#     context = "\n\n".join(retrieved_texts)
#     prompt = f"""
# You are a knowledgeable assistant. Use the provided document context below to answer the user's query accurately and concisely.

# Context:
# {context}

# Question:
# {query_text}

# Answer:
# """

#     # Step 5️⃣: Generate answer using Groq API
#     try:
#         GROQ_API_KEY = os.getenv("GROQ_API_KEY", config.GROQ_API_KEY)
#         if not GROQ_API_KEY:
#             raise ValueError("Missing GROQ_API_KEY")

#         url = "https://api.groq.com/openai/v1/chat/completions"
#         headers = {
#             "Authorization": f"Bearer {GROQ_API_KEY}",
#             "Content-Type": "application/json"
#         }
#         data = {
#             "model": "llama3-8b-8192",  # or another Groq-supported model
#             "messages": [
#                 {"role": "system", "content": "You are a helpful assistant for answering document-based queries."},
#                 {"role": "user", "content": prompt}
#             ],
#             "temperature": 0.3
#         }

#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()

#         answer = response.json()["choices"][0]["message"]["content"]
#         answer = clean_text(answer)
#         log("✅ Generated contextual Groq answer successfully.")
#         return answer, metadatas

#     except Exception as e:
#         log(f"❌ Error generating LLM answer: {e}")
#         return f"An error occurred while generating the answer: {e}", []
import os
import requests
from dotenv import load_dotenv
from app.services.vectorstore import get_relevant_chunks
from app.utils.logger import log

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def ask_question(query: str):
    try:
        log("🔍 Step 1: Retrieving relevant chunks for the query...")
        chunks = get_relevant_chunks(query)
        if not chunks:
            log("⚠️ No relevant chunks found in the document.")
            return "No relevant information found for your question."

        log(f"✅ Retrieved {len(chunks)} chunks from vector store.")
        log("🧩 Sample of retrieved chunks:")
        for i, chunk in enumerate(chunks[:3]):  # show first 3 chunks
            log(f"  Chunk {i+1}: {chunk[:200]}...")  # limit output for readability

        # Combine context for the model
        context_text = "\n".join(chunks)

        log("🚀 Step 2: Sending request to Groq API...")
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.1-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant that answers based on document context."},
                {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
            ]
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )

        log(f"📡 Groq API status: {response.status_code}")
        log(f"📨 Groq response preview: {response.text[:500]}")  # first 500 chars only

        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        log("✅ Step 3: Successfully generated Groq answer.")
        return answer

    except requests.exceptions.RequestException as e:
        log(f"❌ Request to Groq API failed: {e}")
        return "Groq API request failed. Check your API key or network."
    except Exception as e:
        log(f"❌ Unexpected error in RAG pipeline: {e}")
        return "Error processing your request."
