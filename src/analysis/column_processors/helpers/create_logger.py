import logging
import os
import datetime

LOGS_FOLDER = '.logs'

def create_logger() -> logging.Logger:
    logger_name = 'my_application_logger'  # Common name for the logger
    logger = logging.getLogger(logger_name)

    # Check if the logger already has handlers to avoid adding them again
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        # Create logs directory if it doesn't exist
        if not os.path.exists(LOGS_FOLDER):
            os.makedirs(LOGS_FOLDER)

        # File handler - logs to a file with a timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_handler = logging.FileHandler(f'{LOGS_FOLDER}/{logger_name}_{timestamp}.log')
        file_format = logging.Formatter('%(asctime)s - %(pathname)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

        # Console handler - logs to the console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(file_format)
        logger.addHandler(console_handler)

    return logger