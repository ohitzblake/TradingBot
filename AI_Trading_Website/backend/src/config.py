import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_PORT = int(os.getenv('API_PORT', 8000))
API_HOST = os.getenv('API_HOST', '0.0.0.0')

# Trading API Keys
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET', '')
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY', '')
ALPACA_API_SECRET = os.getenv('ALPACA_API_SECRET', '')

# News API Key
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')

# CORS Settings
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')