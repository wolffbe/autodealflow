import logging
import json

logger = logging.getLogger(__name__)

def get_msg_as_json(message):
    if message is None:
        logger.warning("Received None message, returning None.")
        return None

    if isinstance(message, dict):
        logger.debug("Message is already a dictionary, returning as is.")
        return message

    if isinstance(message, (bytes, bytearray)):
        message = message.decode('utf-8')
    elif not isinstance(message, str):
        raise ValueError(f"Invalid message type: {type(message).__name__}. Expected str, bytes, or dict.")

    try:
        result = json.loads(message)
        logger.debug("Successfully converted Redis message to JSON.")
        return result
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")

def compile_oracle_message(msg_id, msg_type, email_json, prompt):
    logger.debug("Entering compile_oracle_message")
    
    valid_types = {'is_opp', 'opp'}

    if msg_type not in valid_types:
        raise ValueError(f"Invalid message type: {msg_type}. Valid types are {', '.join(valid_types)}.")

    return {
        "id": msg_id,
        "type": msg_type,
        "email": email_json,
        "prompt": prompt
    }
    
def compile_export_message(msg_id, msg_type, fields):
    logger.debug(f"Compiling export message for msg_id: {msg_id}")
    return {
        "id": msg_id,
        "type": msg_type,
        "fields": fields
    }