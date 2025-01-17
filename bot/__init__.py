# bot/__init__.py

import logging

# Configure logging for the bot package
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Optional: Expose main modules for easier imports
from .handlers import start_handler, backup_handler
from .repository import BackupRepository
