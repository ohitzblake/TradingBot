import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_PORT = int(os.getenv('API_PORT', 8000))
API_HOST = os.getenv('API_HOST', '0.0.0.0')

# OpenAI API Key (replacing other API keys)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# CORS Settings
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

# Mock data settings
USE_MOCK_DATA = os.getenv('USE_MOCK_DATA', 'true').lower() == 'true'