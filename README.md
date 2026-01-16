# RAG with Docling & MCP

This repository contains a Retrieval-Augmented Generation (RAG) system using [Docling](https://github.com/DS4SD/docling) for document ingestion, [Qdrant](https://qdrant.tech/) for vector storage, and is designed to work as a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server.

## Features

- **Document Ingestion**: Uses Docling to parse PDF and other document formats.
- **Vector Search**: Embeds and stores chunks in a local Qdrant instance.
- **RAG Service**: Provides tools to query the knowledge base.
- **MCP Compatible**: Designed to expose tools to LLMs via MCP.

## Prerequisites

- Python 3.10+
- Docker (for Qdrant)

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rag-docling-mcp
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**
   Copy the example environment file and configure your keys:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your `LITELLM_API_KEY`.

## Running the System

### 1. Start Qdrant (Vector Database)
```bash
docker run -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage" qdrant/qdrant
```

### 2. Run the Notebook Tester
Open `tester.ipynb` in VS Code or Jupyter Lab to ingest documents and test queries interactively.

### 3. (Optional) Run as MCP Server
(Instructions to be added based on `src/server.py` implementation)
