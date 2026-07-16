import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Validate API Keys
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found in .env file")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Pinecone Configuration
INDEX_NAME = "intermediate-rag"
NAMESPACE = "pdf-documents" 
