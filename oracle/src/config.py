import os
import logging

logger = logging.getLogger(__name__)

def load_config():
    config = {
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),
        "REDIS_HOST": os.getenv("REDIS_HOST"),
        "REDIS_PORT": os.getenv("REDIS_PORT"),
        "ORACLE_CH": os.getenv("ORACLE_CH"),
        "OPP_CH": os.getenv("OPP_CH"),
        "OPEN_AI_KEY": os.getenv("OPEN_AI_KEY"),
        "OPEN_AI_MODEL": os.getenv("OPEN_AI_MODEL")
    }

    missing_vars = [key for key, value in config.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing configuration in .env file: {', '.join(missing_vars)}")

    try:
        config["REDIS_PORT"] = int(config["REDIS_PORT"])
    except ValueError:
        raise ValueError("Invalid value for REDIS_PORT. It must be an integer.")

    return config