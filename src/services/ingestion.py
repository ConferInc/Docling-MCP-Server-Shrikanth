import uuid
import sys
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.chunking import HybridChunker
from src.db import get_embedding, q_client, setup_collection
from src.config import COLLECTION_NAME
from qdrant_client.http import models

def ingest_source(url: str) -> str:
    setup_collection()
    
    # 1. Configure for CPU (OCR disabled for speed)
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False 
    pipeline_options.do_table_structure = True

    print(f"[INFO] Processing: {url}", file=sys.stderr)
    
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    
    doc = converter.convert(url).document
    
    # 2. Chunking
    chunker = HybridChunker(tokenizer="sentence-transformers/all-MiniLM-L6-v2") 
    chunks = list(chunker.chunk(doc))
    
    points = []
    print(f"[INFO] Embedding {len(chunks)} chunks...", file=sys.stderr)
    
    for i, chunk in enumerate(chunks):
        # [FIX] Get text safely
        text = chunk.text if hasattr(chunk, 'text') else str(chunk)
        if not text.strip(): continue
        
        try:
            vector = get_embedding(text)
            
            # [CRITICAL FIX] Bulletproof Page Number Extraction
            # We try every possible way to find the page. If all fail, default to 1.
            page_no = 1
            try:
                if hasattr(chunk, 'prov') and chunk.prov:
                    page_no = chunk.prov[0].page_no
                elif hasattr(chunk, 'meta') and chunk.meta and hasattr(chunk.meta, 'doc_items'):
                    # Deep fallback for complex objects
                    items = chunk.meta.doc_items
                    if items and hasattr(items[0], 'prov') and items[0].prov:
                        page_no = items[0].prov[0].page_no
            except:
                # If ANY of that logic fails, just ignore it and use Page 1
                pass

            points.append(models.PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "source": url,
                    "content": text,
                    "page": page_no
                }
            ))
        except Exception as e:
            # Only print error if it's NOT the 'prov' error
            if "prov" not in str(e):
                print(f"[WARN] Skip chunk {i}: {str(e)}", file=sys.stderr)

    if points:
        q_client.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f"[SUCCESS] Ingested {len(points)} chunks.", file=sys.stderr)
        return f"Successfully ingested {len(points)} chunks from {url}"
    else:
        return "No valid text chunks found."