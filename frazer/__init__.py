import logging
import logging.config

from dotenv import load_dotenv

logging.config.fileConfig("logging.conf")

load_dotenv()


__version__ = "0.0.1-dev-2025022"
