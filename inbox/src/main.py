import redis
import time
from config import load_config
from logger import setup_logger
from email_importer import process_emails

config = load_config()
logger = setup_logger(config.get("LOG_LEVEL", "INFO"))
redis_client = redis.Redis(config.get("REDIS_HOST"), config.get("REDIS_PORT"), decode_responses=True)

def main():
    
    logger.info("Starting inbox...")
    
    email_credentials = {
        "server": config.get("IMAP_SERVER"),
        "user": config.get("EMAIL_USER"),
        "pw": config.get("EMAIL_PASS")
    }
    
    while True:
        process_emails(email_credentials, redis_client, config.get("OPP_CH"))
        logger.debug(f"Sleeping for {config['POLLING_INTERVAL']} seconds before next poll...")
        time.sleep(int(config['POLLING_INTERVAL']))

if __name__ == "__main__":
    main()