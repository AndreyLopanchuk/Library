import logging
from logging.handlers import RotatingFileHandler

from src.core.config import settings

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    filename=settings.logging.filename, maxBytes=settings.logging.max_bytes, backupCount=settings.logging.backup_count
)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

handler.setFormatter(formatter)

logger.addHandler(handler)
