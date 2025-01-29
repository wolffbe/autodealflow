import logging

def setup_logger(log_level):
    log_level = getattr(logging, str(log_level).upper(), None)
    
    if log_level is None:
        raise ValueError(f"Invalid log level: {log_level}. Use one of the following: DEBUG, INFO, WARNING, ERROR, CRITICAL.")
    
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger("CustomLogger")