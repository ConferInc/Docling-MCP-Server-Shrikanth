import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcp.server.fastmcp import FastMCP
from src.services.ingestion import ingest_source
from src.services.retrieval import query_knowledge_base
from src.db import q_client
from src.config import COLLECTION_NAME

mcp = FastMCP("Internal RAG Server")

@mcp.tool()
def add_knowledge(url: str) -> str:
    """Ingests a PDF/URL into the Qdrant Knowledge Base."""
    try:
        return ingest_source(url)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def ask_knowledge(question: str) -> str:
    """Searches the Knowledge Base for answers."""
    return query_knowledge_base(question)

@mcp.tool()
def check_status() -> str:
    """Checks how many documents are in the database."""
    try:
        count = q_client.count(collection_name=COLLECTION_NAME)
        return f"Database Status: Healthy. Contains {count.count} chunks."
    except Exception as e:
        return f"Database Error: {e}"

if __name__ == "__main__":
    mcp.run()