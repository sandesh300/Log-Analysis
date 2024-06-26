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

# Define log message formats
formats = {
    logging.INFO: "INFO message",
    logging.DEBUG: "DEBUG message",
    logging.ERROR: "ERROR message"
}

# Define log levels to cycle through
log_levels = [logging.INFO, logging.DEBUG, logging.ERROR]

# Dictionary to store HTTP status code counts
status_code_counts = {}

def monitor_log_file(file_path):
    try:
        log_file = Path(file_path)
        if not log_file.exists():
            logger.error(f"Log file '{file_path}' does not exist.")
            return
        if not log_file.is_file():
            logger.error(f"'{file_path}' is not a file.")
            return
        with log_file.open("r") as f:
            # Monitor the log file for new entries
            f.seek(0, 2)  # Move to the end of the file
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)  # Avoid high CPU usage
                    continue
                # Perform log analysis
                analyze_log_entry(line)
    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
    except (FileNotFoundError, IOError) as e:
        logger.error(f"Error opening log file: {e}")
    except KeyboardInterrupt:
        print("\nLog monitoring interrupted. Exiting.")
    except Exception as e:
        logger.error(f"Error monitoring log file: {e}")

def analyze_log_entry(log_entry):
    # Count occurrences of specific keywords or patterns
    keyword = "error"
    if keyword.lower() in log_entry.lower():
        logger.error(f"Found '{keyword}' in log entry: {log_entry.strip()}")

    # Count HTTP status codes
    http_status_pattern = r"HTTP/\d\.\d\"\s(\d{3})"
    match = re.search(http_status_pattern, log_entry)
    if match:
        status_code = match.group(1)
        status_code_counts[status_code] = status_code_counts.get(status_code, 0) + 1

def generate_status_code_report():
    logger.info("Summary of HTTP status codes:")
    for status_code, count in sorted(status_code_counts.items(), key=lambda x: x[1], reverse=True):
        logger.info(f"{status_code}: {count}")

# Main loop to log messages
while True:
    try:
        # Randomly select a log level
        log_level = random.choice(log_levels)

        # Get the log message format for the selected log level
        log_message = formats[log_level]

        # Log the message
        logger.log(log_level, log_message)

        # Sleep for a short interval
        time.sleep(1)
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C)
        print("\nLogging interrupted. Exiting.")
        generate_status_code_report()
        break

monitor_log_file(log_file_path)