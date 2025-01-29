import os
import logging

logger = logging.getLogger(__name__)

def load_config():
    config = {
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),
        "EMAIL_USER": os.getenv("EMAIL_USER"),
        "EMAIL_PASS": os.getenv("EMAIL_PASS"),
        "IMAP_SERVER": os.getenv("IMAP_SERVER"),
        "REDIS_HOST": os.getenv("REDIS_HOST"),
        "REDIS_PORT": os.getenv("REDIS_PORT"),
        "OPP_CH": os.getenv("OPP_CH"),
        "IMBOX_CONFIG": os.getenv("IMBOX_CONFIG"),
        "ATTACHMENTS_DIR": os.getenv("ATTACHMENTS_DIR"),
        "POLLING_INTERVAL": os.getenv("POLLING_INTERVAL"),
    }

    missing_vars = [key for key, value in config.items() if not value and key != "IMBOX_CONFIG"]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    try:
        config["REDIS_PORT"] = int(config["REDIS_PORT"])
        logger.debug(f"REDIS_PORT successfully converted to integer: {config['REDIS_PORT']}")
    except ValueError as e:
        raise ValueError("Invalid value for REDIS_PORT. It must be an integer.") from e

    logger.debug("Configuration loaded successfully.")

    return config