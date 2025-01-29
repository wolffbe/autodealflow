import redis
import json
from logger import setup_logger
from config import load_config
from redis_client import get_redis_msg_from, publish_msg_via_redis
from open_ai import respond_to_prompt

config = load_config()
logger = setup_logger(config.get("LOG_LEVEL", "INFO"))
redis_client = redis.Redis(config.get("REDIS_HOST"), config.get("REDIS_PORT"), decode_responses=True)

def main():
    logger.info("Starting oracle...")

    while True:
        try:
            logger.debug("Waiting for message from Redis channel...")

            msg = get_redis_msg_from(redis_client, config.get("ORACLE_CH"))
            
            if msg:
                msg_type = msg.get("type")
                
                if msg_type in ["is_opp", "opp"]:
                    logger.debug(f"Processing message with type '{msg_type}'.")

                    response_json = respond_to_prompt(config.get("OPEN_AI_KEY"), config.get("OPEN_AI_MODEL"), msg)

                    if msg_type == "is_opp":
                        logger.debug(f"Received 'is_opp' message with ID '{msg.get('id')}'")
                        msg["type"] = "is_opp_rsp"
                        msg["response"] = response_json.choices[0].message.content
                    elif msg_type == "opp":
                        logger.debug(f"Received 'opp' message with ID '{msg.get('id')}'")
                        msg["type"] = "opp_rsp"
                        msg["response"] = json.loads(response_json.choices[0].message.content)
                    
                    publish_msg_via_redis(redis_client, config.get("OPP_CH"), msg)
                    
                    logger.info(f"Processed '{msg_type}' message with ID '{msg.get('id')}'")

                else:
                    logger.debug(f"Received message with unknown type, ignoring...")

            else:
                logger.debug("No message received, continuing to wait.")

        except Exception as e:
            raise ValueError(f"Error during message processing: {e}")

if __name__ == "__main__":
    main()