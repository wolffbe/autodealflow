import redis
from logger import setup_logger
from config import load_config
from redis_client import get_redis_msg_from, publish_msg_via_redis
from message_handler import get_msg_as_json, compile_oracle_message, compile_export_message
from email_parser import parse_email_json_to_text
from prompt_compiler import compile_is_opp_prompt, compile_opp_prompt

config = load_config()
logger = setup_logger(config.get("LOG_LEVEL", "INFO"))
redis_client = redis.Redis(config.get("REDIS_HOST"), config.get("REDIS_PORT"), decode_responses=True)

def handle_email_message(msg_json):
    email_json = parse_email_json_to_text(msg_json["email"])
    is_opp_prompt = compile_is_opp_prompt(
        config.get("IS_OPP_PROMPT_PATH"), email_json, config.get("THESIS")
    )

    oracle_msg = compile_oracle_message(msg_json["id"], "is_opp", email_json, is_opp_prompt)
    publish_msg_via_redis(redis_client, config.get("ORACLE_CH"), oracle_msg)

def handle_is_opp_rsp(msg_json):    
    if msg_json.get("response").lower() == "true":
        opp_prompt = compile_opp_prompt(
            config.get("OPP_PROMPT_PATH"), config.get("OPP_FIELDS"), msg_json["email"]
        )
        oracle_msg = compile_oracle_message(msg_json["id"], "opp", msg_json["email"], opp_prompt)
        publish_msg_via_redis(redis_client, config.get("ORACLE_CH"), oracle_msg)

def handle_opp_rsp(msg_json):    
    msg = compile_export_message(msg_json["id"], "notion_export", msg_json["response"])
    publish_msg_via_redis(redis_client, config.get("NOTION_EXPORT_CH"), msg)

def process_message(msg):
    msg_json = get_msg_as_json(msg)

    if not msg_json or "type" not in msg_json:
        logger.warning("Received an invalid or empty message.")
        return

    msg_type = msg_json["type"].lower() if isinstance(msg_json["type"], str) else None

    if msg_type == "email_import" and "email" in msg_json:
        logger.debug(f"Processing email_import with ID {msg_json['id']}")
        handle_email_message(msg_json)
        logger.info(f"Processed email_import with ID {msg_json['id']}")
    elif msg_type == "is_opp_rsp":
        logger.debug(f"Processing is_opp_rsp with ID {msg_json['id']}")
        handle_is_opp_rsp(msg_json)
        logger.info(f"Processed is_opp_rsp with ID {msg_json['id']}")
    elif msg_type == "opp_rsp":
        logger.debug(f"Processing opp_rsp with ID {msg_json['id']}")
        handle_opp_rsp(msg_json)
        logger.info(f"Processed opp_rsp with ID {msg_json['id']}")
    else:
        logger.warning(f"Unsupported message type: {msg_json['type']}")

def main():
    logger.info("Starting opportunity analysis...")

    while True:
        try:
            msg = get_redis_msg_from(redis_client, config.get("OPP_CH"))
            if msg:
                process_message(msg)
            else:
                logger.debug("No message received, waiting...")
        except Exception as e:
            raise RuntimeError(f"Error during message processing: {e}")

if __name__ == "__main__":
    main()
