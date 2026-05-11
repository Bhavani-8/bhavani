# setup_logger.py

import logging
from datetime import datetime
from pathlib import Path

def setup_logger(module="TA"):
    """
    Proper logger with isolated handlers (file + console).
    Does NOT rely on basicConfig().
    """
    
    module_log_dir = Path(f"logs/{module}_logs")
    module_log_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = module_log_dir / f"{module}_log_{timestamp}.txt"

    # Create dedicated logger
    logger = logging.getLogger(f"{module}_logger")
    logger.setLevel(logging.DEBUG)  # capture ALL logs
    
    # Prevent duplicate handlers on multiple calls
    logger.handlers.clear()
    
    # Prevent logs from propagating to root logger
    logger.propagate = False

    # File handler
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)  # everything goes to file
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    # Add handlers
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info(f"📝 Logging initialized → {log_file}")
    return logger