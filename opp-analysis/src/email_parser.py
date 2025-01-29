import os
import logging
from pdf_parser import parse_pdf_to_text

logger = logging.getLogger(__name__)

class AttachmentError(Exception):
    pass

def validate_attachment_directory(attachment_folder):
    if not attachment_folder:
        raise ValueError("Attachment directory is missing.")
    
    if not os.path.exists(attachment_folder):
        raise FileNotFoundError(f"Attachment directory does not exist: {attachment_folder}")

    if not os.path.isdir(attachment_folder):
        raise NotADirectoryError(f"Attachment path is not a directory: {attachment_folder}")

    if not os.access(attachment_folder, os.R_OK):
        raise PermissionError(f"Attachment directory is not accessible: {attachment_folder}")

    logger.debug(f"Attachment directory validated: {attachment_folder}")

def process_pdf_attachments(attachment_folder):
    attachments_as_text = []

    for entry in os.scandir(attachment_folder):
        if entry.is_file() and entry.name.lower().endswith(".pdf"):
            try:
                logger.debug(f"Processing PDF attachment: {entry.name}")
                attachment_text = parse_pdf_to_text(entry.path)
                logger.debug(f"Extracted text from {entry.name}: {attachment_text[:200]}...")
                attachments_as_text.append(attachment_text)
            except Exception as e:
                raise AttachmentError(f"Error processing PDF attachment {entry.name}: {e}") from e

    return attachments_as_text

def parse_email_json_to_text(email_json):
    logger.debug("Entering parse_email_json_to_text function")

    attachment_folder = email_json.get("attachment_directory")
    
    if attachment_folder:
        try:
            validate_attachment_directory(attachment_folder)
            logger.debug(f"Processing attachments in: {attachment_folder}")
            attachments_as_text = process_pdf_attachments(attachment_folder)
            logger.debug(f"Processed {len(attachments_as_text)} PDF(s).")
        except (ValueError, FileNotFoundError, NotADirectoryError, PermissionError, AttachmentError) as e:
            raise RuntimeError(f"Error processing attachments: {e}") from e

        email_json["attachments_as_text"] = attachments_as_text
        del email_json["attachment_directory"]
    else:
        logger.debug("No attachment directory found, skipping PDF processing.")

    logger.debug("Exiting parse_email_json_to_text function")
    return email_json
