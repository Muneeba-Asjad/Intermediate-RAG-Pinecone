from pypdf import PdfReader


def load_pdf(pdf_file):
    pages_data = []

    try:
        reader = PdfReader(pdf_file)

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            if text:
                clean_text = " ".join(text.split())

                pages_data.append({
                    "page_number": page_number,
                    "text": clean_text
                })

        return pages_data

    except Exception as e:
        raise Exception(f"PDF Loading Error: {str(e)}")