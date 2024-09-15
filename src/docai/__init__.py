import logging
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

# Suppress datashaper logs
logging.getLogger("datashaper").setLevel(logging.WARNING)
logging.getLogger("byaldi").setLevel(logging.WARNING)
logging.getLogger("numba").setLevel(logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("pdfminer").setLevel(logging.WARNING)
logging.getLogger("layoutparser").setLevel(logging.WARNING)
logging.getLogger("pikepdf").setLevel(logging.WARNING)
