import json
import logging

logger = logging.getLogger(__name__)

def publish_msg_via_redis(redis_client, receiver, msg):
    try:
        logger.debug(f"Sending message to {receiver}.")
        redis_client.rpush(receiver, json.dumps(msg, default=str))
    except Exception as e:
        raise ValueError(f"Error sending message to {receiver}: {e}")

def get_redis_msg_from(redis_client, channel_name):
    try:
        message = redis_client.blpop(channel_name, timeout=0)
        if message:
            logger.debug(f"Received message from channel {channel_name}.")
            return json.loads(message[1])
        return None
    except Exception as e:
        raise ValueError(f"Error retrieving message from channel {channel_name}: {e}")