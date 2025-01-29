import os
import logging

logger = logging.getLogger(__name__)

def load_config():
    config = {
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),
        "REDIS_HOST": os.getenv("REDIS_HOST"),
        "REDIS_PORT": os.getenv("REDIS_PORT"),
        "OPP_CH": os.getenv("OPP_CH"),
        "ORACLE_CH": os.getenv("ORACLE_CH"),
        "IS_OPP_PROMPT_PATH": os.getenv("IS_OPP_PROMPT_PATH"),
        "THESIS": os.getenv("THESIS"),
        "OPP_PROMPT_PATH": os.getenv("OPP_PROMPT_PATH"),
        "OPP_FIELDS": os.getenv("OPP_FIELDS"),
        "NOTION_EXPORT_CH": os.getenv("NOTION_EXPORT_CH")
    }

    missing_vars = [key for key, value in config.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    try:
        config["REDIS_PORT"] = int(config["REDIS_PORT"])
    except ValueError as e:
        raise ValueError("Invalid value for REDIS_PORT. It must be an integer.") from e

    logger.debug("Configuration loaded successfully.")
    return config