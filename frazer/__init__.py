import logging
import logging.config

from dotenv import load_dotenv

logging.config.fileConfig("logging.conf")

load_dotenv()
