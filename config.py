import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found in .env file")

INDEX_NAME = "intermediate-rag"
NAMESPACE = "pdf-documents"