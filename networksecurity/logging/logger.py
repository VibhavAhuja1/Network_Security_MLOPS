import logging
import os
import sys
from datetime import datetime

# ── Anchor to project root (2 levels up from networksecurity/logging/logger.py) ──
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# ── Config ────────────────────────────────────────────────────────────────────
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
#LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE = "networksecurity.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

os.makedirs(LOG_DIR, exist_ok=True)

# ── Formatter ─────────────────────────────────────────────────────────────────
FMT = "[ %(asctime)s ] %(levelname)-8s %(name)s:%(lineno)d — %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"

formatter = logging.Formatter(fmt=FMT, datefmt=DATE_FMT)

# ── Handlers ──────────────────────────────────────────────────────────────────
file_handler = logging.FileHandler(LOG_FILE_PATH, encoding="utf-8")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

# ── Root logger ───────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[file_handler, stream_handler],
)

# ── Public helper ─────────────────────────────────────────────────────────────
def get_logger(name: str = __name__) -> logging.Logger:
    return logging.getLogger(name)