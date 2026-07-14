import streamlit as st

from pdf_loader import load_pdf
from chunker import create_chunks
from pinecone_db import store_chunks
from retriever import retrieve_context
from generator import generate_answer
from logger import log_query


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Intermediate RAG System",
    page_icon="📘",
    layout="wide"
)

st.title("📘 Intermediate RAG System")

st.write(
    "PDF Question Answering using Pinecone Vector Database "
    "and Local LLM"
)


# ---------------- SESSION STATE ----------------

if "history" not in st.session_state:
    st.session_state.history = []


# ---------------- SIDEBAR SETTINGS ----------------

st.sidebar.header("⚙️ RAG Settings")


chunk_size = st.sidebar.slider(
    "Chunk Size",
    min_value=100,
    max_value=1000,
    value=500,
    step=100
)


top_k = st.sidebar.slider(
    "Top-K Results",
    min_value=1,
    max_value=10,
    value=3
)


threshold = st.sidebar.slider(
    "Similarity Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.05
)


page_filter = st.sidebar.number_input(
    "Filter by Page (0 = All Pages)",
    min_value=0,
    value=0,
    step=1
)


# ---------------- PDF UPLOAD ----------------

st.subheader("📄 Upload Documents")


uploaded_files = st.file_uploader(
    "Upload PDF Documents (Maximum 20 MB per file)",
    type=["pdf"],
    accept_multiple_files=True
)


if uploaded_files:

    if st.button("📥 Process Documents"):

        try:

            total_chunks = 0
            processed_documents = 0

            with st.spinner("Processing PDFs..."):

                for pdf_file in uploaded_files:

                    # 20 MB File Limit

                    if pdf_file.size > 20 * 1024 * 1024:

                        st.error(
                            f"❌ {pdf_file.name} exceeds "
                            "the 20 MB file limit."
                        )

                        continue


                    # PDF Text Extraction

                    pages = load_pdf(pdf_file)


                    if not pages:

                        st.warning(
                            f"⚠️ No text found in "
                            f"{pdf_file.name}"
                        )

                        continue


                    # Text Chunking

                    chunks = create_chunks(
                        pages,
                        chunk_size=chunk_size
                    )


                    # Store Chunks in Pinecone

                    count = store_chunks(
                        chunks,
                        pdf_file.name
                    )


                    total_chunks += count

                    processed_documents += 1


            if processed_documents > 0:

                st.success(
                    f"✅ {processed_documents} document(s) "
                    f"processed successfully. "
                    f"{total_chunks} chunks stored in Pinecone."
                )


        except Exception as e:

            st.error(
                f"❌ Processing Error: {str(e)}"
            )


# ---------------- DIVIDER ----------------

st.divider()


# ---------------- QUESTION SECTION ----------------

st.subheader("💬 Ask a Question")


query = st.text_input(
    "Enter your question about the uploaded PDF:"
)


if st.button("🔍 Get Answer"):

    if not query.strip():

        st.warning(
            "⚠️ Please enter a question."
        )


    else:

        try:

            with st.spinner(
                "Searching document..."
            ):


                # Semantic Retrieval

                retrieved_chunks = retrieve_context(

                    query=query,

                    top_k=top_k,

                    threshold=threshold,

                    page_filter=(
                        page_filter
                        if page_filter > 0
                        else None
                    )

                )


                # Generate Answer

                answer = generate_answer(
                    query,
                    retrieved_chunks
                )


                # Log Query

                log_query(
                    query,
                    answer
                )


            # ---------------- ANSWER ----------------

            st.subheader("🤖 Answer")


            st.info(
                answer
            )


            # ---------------- SOURCE REFERENCES ----------------

            st.subheader(
                "📚 Source References"
            )


            if retrieved_chunks:

                for chunk in retrieved_chunks:

                    with st.expander(

                        f"📄 {chunk['document_name']} "
                        f"| Page {chunk['page_number']} "
                        f"| Similarity Score: "
                        f"{chunk['score']:.3f}"

                    ):


                        st.write(
                            "**Relevant Excerpt:**"
                        )


                        st.write(
                            chunk["text"][:500]
                        )


            else:

                st.warning(
                    "No relevant source chunks found."
                )


            # ---------------- SAVE QUERY HISTORY ----------------

            st.session_state.history.append({

                "question": query,

                "answer": answer

            })


        except Exception as e:

            st.error(
                f"❌ Retrieval Error: {str(e)}"
            )


# ---------------- DIVIDER ----------------

st.divider()


# ---------------- QUERY HISTORY ----------------

st.subheader("🕘 Query History")


if st.session_state.history:

    for item in reversed(
        st.session_state.history
    ):


        st.write(
            f"**Question:** "
            f"{item['question']}"
        )


        st.write(
            f"**Answer:** "
            f"{item['answer']}"
        )


        st.divider()


else:

    st.write(
        "No queries asked yet."
    )