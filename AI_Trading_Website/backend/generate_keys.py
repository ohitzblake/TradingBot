#!/usr/bin/env python
import os
import secrets
import string
from pathlib import Path

def generate_random_key(length=32):
    """Generate a random API key of specified length"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def update_env_file():
    """Update or create .env file with generated API keys"""
    env_path = Path('.env')
    
    # Read existing .env file if it exists
    env_vars = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    
    # Generate new keys if they don't exist
    if 'BINANCE_API_KEY' not in env_vars or not env_vars['BINANCE_API_KEY']:
        env_vars['BINANCE_API_KEY'] = generate_random_key()
    
    if 'BINANCE_API_SECRET' not in env_vars or not env_vars['BINANCE_API_SECRET']:
        env_vars['BINANCE_API_SECRET'] = generate_random_key(64)
    
    if 'ALPACA_API_KEY' not in env_vars or not env_vars['ALPACA_API_KEY']:
        env_vars['ALPACA_API_KEY'] = generate_random_key()
    
    if 'ALPACA_API_SECRET' not in env_vars or not env_vars['ALPACA_API_SECRET']:
        env_vars['ALPACA_API_SECRET'] = generate_random_key(64)
    
    if 'NEWS_API_KEY' not in env_vars or not env_vars['NEWS_API_KEY']:
        env_vars['NEWS_API_KEY'] = generate_random_key()
    
    # Ensure other required variables exist
    if 'API_PORT' not in env_vars:
        env_vars['API_PORT'] = '8000'
    
    if 'API_HOST' not in env_vars:
        env_vars['API_HOST'] = '0.0.0.0'
    
    if 'FRONTEND_URL' not in env_vars:
        env_vars['FRONTEND_URL'] = 'http://localhost:3000'
    
    # Write updated .env file
    with open(env_path, 'w') as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print("API keys generated and saved to .env file")
    print("\nIMPORTANT: These are randomly generated keys for development purposes.")
    print("For production use, replace them with actual API keys from the respective services.")
    print("\nGenerated keys:")
    print(f"BINANCE_API_KEY={env_vars['BINANCE_API_KEY']}")
    print(f"ALPACA_API_KEY={env_vars['ALPACA_API_KEY']}")
    print(f"NEWS_API_KEY={env_vars['NEWS_API_KEY']}")

if __name__ == "__main__":
    update_env_file()