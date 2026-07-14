from pinecone import Pinecone
from config import PINECONE_API_KEY, INDEX_NAME, NAMESPACE

pc = Pinecone(api_key=PINECONE_API_KEY)


def get_index():
    if not pc.has_index(INDEX_NAME):
        print("Creating Pinecone index...")

        pc.create_index_for_model(
            name=INDEX_NAME,
            cloud="aws",
            region="us-east-1",
            embed={
                "model": "llama-text-embed-v2",
                "field_map": {
                    "text": "chunk_text"
                },
                "metric": "cosine"
            }
        )

    return pc.Index(INDEX_NAME)


def store_chunks(chunks, document_name):
    index = get_index()

    records = []

    for chunk in chunks:
        records.append({
            "_id": f"{document_name}-{chunk['chunk_id']}",
            "chunk_text": chunk["text"],
            "page_number": chunk["page_number"],
            "document_name": document_name,
            "chunk_id": chunk["chunk_id"]
        })

    for start in range(0, len(records), 90):
        batch = records[start:start + 90]

        index.upsert_records(
            namespace=NAMESPACE,
            records=batch
        )

    return len(records)