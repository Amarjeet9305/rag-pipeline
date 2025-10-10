# backend/app/services/embeddings.py
from groq import Groq
import app.config as config

# Absolute import from app package

# -----------------------------
# Initialize Groq client
# -----------------------------
try:
    client = Groq(api_key=config.GROQ_API_KEY)
except Exception as e:
    raise RuntimeError(f"Failed to initialize Groq client: {e}")


# -----------------------------
# Generate embeddings
# -----------------------------
def create_embeddings(texts, model="nomic-embed-text-v1.5"):
    """
    Generate embeddings for a list of text chunks using Groq API.
    
    Args:
        texts (list[str] or str): Text(s) to embed.
        model (str): Groq embedding model.
    
    Returns:
        list[list[float]]: Embeddings for each text chunk.
    """
    if not isinstance(texts, list):
        texts = [texts]

    try:
        response = client.embeddings.create(input=texts, model=model)
        embeddings = [item.embedding for item in response.data]
        return embeddings
    except Exception as e:
        raise RuntimeError(f"Failed to create embeddings: {e}")


# -----------------------------
# Generate answer from LLM
# -----------------------------
def generate_answer(prompt, model="gpt-like-model", max_tokens=512):
    """
    Generate a response from the LLM using Groq API.
    
    Args:
        prompt (str): Text prompt.
        model (str): Groq LLM model name.
        max_tokens (int): Max tokens to generate.
    
    Returns:
        str: LLM-generated response.
    """
    try:
        response = client.completions.create(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens
        )
        # Return first choice text if available
        return response.choices[0].text if response.choices else ""
    except Exception as e:
        raise RuntimeError(f"Failed to generate LLM answer: {e}")
