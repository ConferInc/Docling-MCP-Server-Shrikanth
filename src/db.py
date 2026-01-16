from typing import List
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models
from src.config import *

# 1. Initialize Clients
# We use the standard OpenAI client but point it to YOUR server
ai_client = OpenAI(api_key=LITELLM_API_KEY, base_url=LITELLM_BASE_URL)
q_client = QdrantClient(url=QDRANT_URL)

def get_embedding(text: str) -> List[float]:
    """Generates vector using LiteLLM."""
    # Remove newlines to avoid tokenization artifacts
    text = text.replace("\n", " ")
    return ai_client.embeddings.create(input=[text], model=EMBEDDING_MODEL).data[0].embedding

def setup_collection():
    """Creates Qdrant collection if missing."""
    if not q_client.collection_exists(COLLECTION_NAME):
        q_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE
            )
        )