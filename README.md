# Log Monitoring and Analysis Script

This script monitors a specified log file for new entries and performs basic analysis on the log entries, such as counting occurrences of specific keywords or patterns and HTTP status codes.

## Prerequisites

- Python 3.x

## Dependencies

The script does not require any external dependencies. It uses the following built-in Python modules:

- `logging`: For logging and log file handling.
- `time`: For introducing delays in the monitoring loop.
- `random`: For randomly selecting log levels.
- `re`: For regular expression pattern matching to detect HTTP status codes.
- `argparse`: For parsing command-line arguments.
- `configparser`: For reading configuration settings from a file.
- `pathlib`: For cross-platform path handling.

## Usage

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Create a `config.ini` file in the project directory with the following content:

config.ini
[DEFAULT]
log_file = app.log
log_level = DEBUG
log_format = %(asctime)s [%(levelname)s] %(message)s

### Run the script with the desired options:

Copy code
python log_monitor.py [--config CONFIG_FILE] [--log-file LOG_FILE]

- -config CONFIG_FILE: Specify the path to the configuration file (optional).
- -log-file LOG_FILE: Specify the path to the log file to be monitored and analyzed (optional).
  
If no command-line arguments are provided, the script will use the default settings from the config.ini file.

- The script will start logging messages at different levels (INFO, DEBUG, and ERROR) to the console and the specified log file.
- It will also monitor the log file for new entries and perform basic analysis, such as counting occurrences of specific keywords or patterns and HTTP status codes.
- To stop the script, press Ctrl+C in the terminal or command prompt.
- Upon interruption, the script will generate a summary report of the top HTTP status codes encountered.
