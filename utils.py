from pypdf import PdfReader

def get_file_path(pdf_upload) -> str:
    if isinstance(pdf_upload, str):
        return pdf_upload
    elif hasattr(pdf_upload, "value") and isinstance(pdf_upload.value, str):
        return pdf_upload.value
    return ""

async def pdf_to_text_converter(pdf_file_path) -> str:
    """Convert a given PDF containing text to a string of text (up to 500 words)."""
    max_words = 500

    if not pdf_file_path:
        return ""

    print(f"File path: {pdf_file_path}")
    reader = PdfReader(pdf_file_path)
    words: list[str] = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        if not page_text.strip():
            continue

        words.extend(page_text.split())
        if len(words) >= max_words:
            break

    return " ".join(words[:max_words]) if words else ""
