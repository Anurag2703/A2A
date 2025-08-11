# ───────────────────────────────────────────────────────────────
# File: backend/utils/file_parser.py
# Purpose: Decode and extract text from base64-encoded files
# ───────────────────────────────────────────────────────────────

import base64
import os
import io
import mimetypes
import traceback

from PIL import Image
import pytesseract
from pdfminer.high_level import extract_text as pdfminer_extract_text
from pdf2image import convert_from_path

from models.task import TaskResponse



# ──────────────── parse_file_to_text ────────────────
def parse_file_to_text(file_path: str) -> str:
    """
    Reads a file and returns extracted text.
    - PDF: Extracts text via pdfminer; falls back to OCR if empty.
    - TXT: Reads raw text.
    - DOCX: Reads paragraphs.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    # Handle PDF
    if ext == ".pdf":
        # First try pdfminer
        text = pdfminer_extract_text(file_path).strip()
        if text:
            return text

        # If no text, fall back to OCR
        images = convert_from_path(file_path)
        ocr_text = []
        for img in images:
            ocr_text.append(pytesseract.image_to_string(img))
        return "\n".join(ocr_text)

    # Handle TXT
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    # Handle DOCX
    elif ext == ".docx":
        import docx
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        raise ValueError(f"Unsupported file type: {ext}")



# ──────────────── Identify MIME Type from base64 ────────────────
def get_mime_type(base64_str: str) -> str:
    header = base64_str.split(',')[0]
    if "pdf" in header:
        return "application/pdf"
    elif "image" in header:
        return "image/png" if "png" in header else "image/jpeg"
    return "unknown"



# ──────────────── Decode Base64 to Plain Text ────────────────
def decode_base64_to_text(base64_str: str) -> str:
    try:
        mime_type = get_mime_type(base64_str)
        base64_data = base64_str.split(",")[-1]
        decoded_data = base64.b64decode(base64_data)

        if mime_type == "application/pdf":
            return extract_text(io.BytesIO(decoded_data))

        elif mime_type.startswith("image"):
            image = Image.open(io.BytesIO(decoded_data))
            return pytesseract.image_to_string(image)

        return "Unsupported file type."

    except Exception as e:
        tb = traceback.format_exc()
        return TaskResponse(success=False, error=f"{e}\n\nTraceback:\n{tb}")
