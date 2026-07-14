import ollama


NOT_FOUND_MESSAGE = (
    "The answer is not available in the provided document."
)


def generate_answer(query, retrieved_chunks):

    if not retrieved_chunks:
        return NOT_FOUND_MESSAGE

    context = "\n\n".join(
        [
            f"[Page {chunk['page_number']}]\n{chunk['text']}"
            for chunk in retrieved_chunks
        ]
    )

    prompt = f"""
You are a document question answering assistant.

RULES:
1. Answer ONLY from the provided document context.
2. Do not use outside knowledge.
3. Do not guess or make up information.
4. If the answer is not clearly available in the context, reply exactly:
"{NOT_FOUND_MESSAGE}"
5. Keep the answer clear and concise.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""

    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response["message"]["content"].strip()

        return answer

    except Exception as e:
        return f"LLM Error: {str(e)}"