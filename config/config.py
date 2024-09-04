import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ['true', '1']
    LOG_DIR = os.getenv('LOG_DIR', 'logs')
    VALID_EXCHANGES = ["B3", "NYSE", "NASDAQ", "LSE", "TSE", "HKSE"]
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
