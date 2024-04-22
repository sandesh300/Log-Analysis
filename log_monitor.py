import logging
import time
import random
import re
import argparse
from configparser import ConfigParser
from pathlib import Path

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Log Monitoring and Analysis Script")
parser.add_argument("-c", "--config", help="Path to the configuration file")
parser.add_argument("-l", "--log-file", help="Path to the log file")
args = parser.parse_args()

# Read configuration settings from a file
config = ConfigParser(interpolation=None)  # Disable interpolation
if args.config:
    config.read(args.config)
else:
    config.read("config.ini")

# Get configuration settings
log_file_path = args.log_file or config.get("DEFAULT", "log_file", fallback="app.log")
log_level = config.get("DEFAULT", "log_level", fallback="DEBUG")
log_format = config.get("DEFAULT", "log_format", fallback="%(asctime)s [%(levelname)s] %(message)s")

# Configure logging
logging.basicConfig(
    level=log_level,
    format=log_format,
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)