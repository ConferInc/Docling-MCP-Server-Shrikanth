import sys
from src.db import get_embedding, q_client
from src.config import COLLECTION_NAME

def query_knowledge_base(query: str) -> str:
    # 1. Embed the Question
    try:
        vector = get_embedding(query)
    except Exception as e:
        return f"❌ Embedding Error: {str(e)}"

    # 2. Search using the robust 'query_points' method
    try:
        # 'query_points' is the low-level API that always exists
        results = q_client.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=5,
            with_payload=True # We must explicitly ask for the text back
        ).points  # Note: The results are inside the .points attribute
        
    except Exception as e:
        return f"❌ Retrieval Error: {str(e)}"

    # 3. Format Output
    if not results:
        return "No relevant information found."
        
    response = []
    for hit in results:
        # In query_points, payload is an attribute, not a dictionary
        payload = hit.payload
        if payload:
            source = payload.get("source", "Unknown")
            content = payload.get("content", "")
            page = payload.get("page", "?")
            response.append(f"---\n📄 Source: {source} (Page {page})\n{content}\n")
        
    return "\n".join(response)