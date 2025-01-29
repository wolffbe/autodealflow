import logging
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

def parse_pdf_to_text(pdf_path):
    logger.debug(f"Starting PDF text extraction for {pdf_path}")

    try:
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])

            preview_text = text[:100] if text else "(No text extracted)"
            logger.debug(f"Successfully converted PDF to text: {pdf_path} - Preview: {preview_text}")

            return text

    except Exception as e:
        raise ValueError(f"Error converting PDF {pdf_path}: {e}")

    finally:
        logger.debug(f"Completed PDF text extraction for {pdf_path}")