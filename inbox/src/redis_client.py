import json
import logging

logger = logging.getLogger(__name__)

def publish_msg_via_redis(redis_client, receiver, msg):
    try:
        logger.debug(f"Sending {msg['type']} {msg['id']} to {receiver}.")
        redis_client.rpush(receiver, json.dumps(msg, default=str))
    except Exception as e:
        raise RuntimeError(f"Error sending message to {receiver}: {e}") from e