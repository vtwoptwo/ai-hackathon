# Logger for the processing

import logging
import os
import datetime

LOGS_FOLDER = '.logs'


def create_logger():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    logger_name = f'logger_{timestamp}'
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Create logs directory if it doesn't exist
    if not os.path.exists(LOGS_FOLDER):
        os.makedirs(LOGS_FOLDER)

    # File handler - logs to a file
    file_handler = logging.FileHandler(f'{LOGS_FOLDER}/{logger_name}.log')
    file_format = logging.Formatter('%(asctime)s - %(pathname)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # Console handler - logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(file_format)
    logger.addHandler(console_handler)

    return logger
