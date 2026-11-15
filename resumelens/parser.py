"""Read resume text from PDF, TXT or raw string."""
import io
import re


def clean(text: str) -> str:
    text = text.replace("\u2022", " ").replace("\t", " ")
    return re.sub(r"[ ]{2,}", " ", text).strip()


def read_resume(file_or_text) -> str:
    """Accepts a string, a bytes object, or a file-like object (PDF or text)."""
    if isinstance(file_or_text, str):
        return clean(file_or_text)
    data = file_or_text.read() if hasattr(file_or_text, "read") else file_or_text
    if data[:4] == b"%PDF":
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(data))
        return clean("\n".join(page.extract_text() or "" for page in reader.pages))
    return clean(data.decode("utf-8", errors="ignore"))
