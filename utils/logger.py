# utils/logger.py
import logging
import sys
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:          # avoid duplicate handlers on re-import
        return logger

    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)

    # File handler (all levels)
    file = logging.FileHandler(LOG_DIR / "test_run.log", mode="a", encoding="utf-8")
    file.setLevel(logging.DEBUG)
    file.setFormatter(fmt)

    logger.addHandler(console)
    logger.addHandler(file)
    logger.propagate = False     # prevent double logging via root logger
    return logger