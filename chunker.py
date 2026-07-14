def create_chunks(pages_data, chunk_size=500):
    chunks = []
    chunk_id = 0

    for page in pages_data:
        page_number = page["page_number"]
        text = page["text"]

        words = text.split()

        for start in range(0, len(words), chunk_size):
            chunk_words = words[start:start + chunk_size]
            chunk_text = " ".join(chunk_words)

            if chunk_text.strip():
                chunks.append({
                    "chunk_id": f"chunk-{chunk_id}",
                    "page_number": page_number,
                    "text": chunk_text
                })

                chunk_id += 1

    return chunks