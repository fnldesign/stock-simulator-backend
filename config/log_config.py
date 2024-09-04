import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(log_dir='logs', log_file='app.log', level=logging.INFO):
    """
    Sets up logging configuration for the application.
    
    Parameters:
    - log_dir (str): The directory where log files will be stored.
    - log_file (str): The log file name.
    - level (int): The logging level (e.g., logging.INFO).
    
    Returns:
    - logger: Configured logger instance.
    """
    # Ensure the logging directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Setup file handler with rotation
    log_file_path = os.path.join(log_dir, log_file)
    file_handler = RotatingFileHandler(log_file_path, maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(level)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(file_handler)
    
    # Return the configured logger
    return logger
