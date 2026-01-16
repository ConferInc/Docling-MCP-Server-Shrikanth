import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- LITELLM SETTINGS ---
# Your Production Proxy URL
LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL", "https://litellm.confersolutions.ai")
# Your Shared Internal Key
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY")

if not LITELLM_API_KEY:
    # Fallback/Warning (optional, or just raise error)
    # Raising error is better to ensure user knows config is missing
    print("⚠️ WARNING: LITELLM_API_KEY not found in environment variables.")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# --- QDRANT SETTINGS ---
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "internal_knowledge_base"
VECTOR_SIZE = 1536