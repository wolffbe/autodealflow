import hashlib
import os
import logging
from config import load_config

config = load_config()
logger = logging.getLogger(__name__)

def get_hashed_directory(email_id):
    if not email_id:
        return None  

    hash_value = hashlib.sha1(email_id.encode()).hexdigest()[:5]
    attachments_dir = config.get("ATTACHMENTS_DIR")

    if not attachments_dir:
        raise ValueError("Missing required environment variable: ATTACHMENTS_DIR")
    
    folder_hash = os.path.join(attachments_dir, hash_value)
    os.makedirs(folder_hash, exist_ok=True)
    
    logger.debug(f"Created directory for attachments: {folder_hash}")
    return folder_hash

def process_pdf_attachments(message):
    email_id = str(getattr(message, "message_id", None))
    
    if not hasattr(message, 'attachments') or not message.attachments:
        return None

    folder_path = get_hashed_directory(email_id)

    if not folder_path:
        return None  

    for attachment in message.attachments:
        if attachment['filename'].lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, attachment['filename'])
            
            with open(file_path, "wb") as pdf_file:
                pdf_file.write(attachment['content'].read())

            logger.debug(f"Saved PDF attachment: {file_path}")
    
    return folder_path