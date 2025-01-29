import socket
import logging
import uuid
from imbox import Imbox
from attachment_handler import process_pdf_attachments
from redis_client import publish_msg_via_redis

logger = logging.getLogger(__name__)

def process_emails(email_credentials, redis_client, receiver):
    server = email_credentials.get("server")
    user = email_credentials.get("user")
    pw = email_credentials.get("pw")

    if not server or not user or not pw:
        raise ValueError("Missing required email credentials: 'server', 'user', or 'pw'.")

    logger.debug(f"Connecting to IMAP server: {server}")
    try:
        with Imbox(server, user, pw, ssl=True) as imbox:
            logger.debug(f"Successfully connected to IMAP server: {server}")
            
            for _, message in imbox.messages():
                message_id = getattr(message, 'message_id', 'Unknown')
                logger.debug(f"Processing email with message ID: {message_id}")
                
                attachment_directory = process_pdf_attachments(message)
                
                msg = {
                    "id": uuid.uuid4(),
                    "type": "email_import",
                    "email": {
                        "email_message_id": str(getattr(message, "message_id", None)),
                        "sent_from": str(getattr(message, "sent_from", None)),
                        "sent_to": str(getattr(message, "sent_to", None)),
                        "subject": str(getattr(message, "subject", None)),
                        "headers": str(getattr(message, "headers", None)),
                        "date": str(getattr(message, "date", None)),
                        "plain_body": message.body.get('plain') if hasattr(message, "body") else None,
                    }
                }

                if attachment_directory:
                    msg["email"]["attachment_directory"] = attachment_directory

                logger.debug(f"Publishing message with ID: {msg['id']}")
                publish_msg_via_redis(redis_client, receiver, msg)
                
                logger.info(f"Processed email with ID: {msg['id']}")

    except (socket.gaierror, ConnectionRefusedError) as e:
        raise ConnectionError(f"Error connecting to the IMAP server: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error while processing emails: {e}") from e