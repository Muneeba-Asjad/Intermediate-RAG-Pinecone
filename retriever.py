from pinecone_db import get_index
from config import NAMESPACE


def retrieve_context(query, top_k=3, threshold=0.3, page_filter=None):
    index = get_index()

    search_filter = None

    if page_filter is not None:
        search_filter = {
            "page_number": {"$eq": page_filter}
        }

    results = index.search(
        namespace=NAMESPACE,
        top_k=top_k,
        inputs={"text": query},
        filter=search_filter,
        fields=[
            "chunk_text",
            "page_number",
            "document_name",
            "chunk_id"
        ]
    )

    retrieved_chunks = []

    hits = results.result.hits

    for hit in hits:
        score = getattr(hit, "score", None)

        if score is None:
            score = getattr(hit, "score_", 0.0)

        fields = hit.fields

        if float(score) >= threshold:
            retrieved_chunks.append({
                "text": fields.get("chunk_text", ""),
                "page_number": fields.get("page_number", "Unknown"),
                "document_name": fields.get("document_name", "Unknown"),
                "chunk_id": fields.get("chunk_id", "Unknown"),
                "score": float(score)
            })

    return retrieved_chunks