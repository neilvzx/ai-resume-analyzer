"""
app/services/pdf_parser.py
Extracts text from a PDF file using pdfplumber.
"""

import pdfplumber


class PDFParseError(Exception):
    pass


def extract_text_from_pdf(file_path: str) -> tuple[str, int]:
    try:
        text_chunks = []
        with pdfplumber.open(file_path) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_chunks.append(page_text)
    except Exception as e:
        raise PDFParseError(f"Failed to open/parse PDF: {e}")

    full_text = "\n".join(text_chunks).strip()

    if not full_text:
        raise PDFParseError(
            "No extractable text found in PDF (it may be a scanned image without OCR)."
        )

    return full_text, page_count
