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
        log(" Step 1: Retrieving relevant chunks for the query...")
        chunks = get_relevant_chunks(query)
        if not chunks:
            log(" No relevant chunks found in the document.")
            return "No relevant information found for your question."

        log(f" Retrieved {len(chunks)} chunks from vector store.")
        log(" Sample of retrieved chunks:")
        for i, chunk in enumerate(chunks[:3]):  # show first 3 chunks
            log(f"  Chunk {i+1}: {chunk[:200]}...")  # limit output for readability

        # Combine context for the model
        context_text = "\n".join(chunks)

        log(" Step 2: Sending request to Groq API...")
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

        log(f" Groq API status: {response.status_code}")
        log(f" Groq response preview: {response.text[:500]}")  # first 500 chars only

        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        log(" Step 3: Successfully generated Groq answer.")
        return answer

    except requests.exceptions.RequestException as e:
        log(f" Request to Groq API failed: {e}")
        return "Groq API request failed. Check your API key or network."
    except Exception as e:
        log(f" Unexpected error in RAG pipeline: {e}")
        return "Error processing your request."

