import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_root_endpoint():
    """Test the root endpoint to check if the API is running."""
    try:
        response = requests.get("http://localhost:8000/")
        print(f"Root endpoint status code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing root endpoint: {e}")
        return False

def main():
    print("\n===== Testing AI Trading Backend =====\n")
    
    # Check if backend is running
    if not test_root_endpoint():
        print("\nBackend is not running or not responding. Please start the backend first.")
        print("Run: python src/main.py")
        return
    
    print("\n✅ Backend is running successfully!")
    
    # Check OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key or openai_key == "your_openai_api_key_here":
        print("\n⚠️ Warning: OpenAI API key is not set or is using the default value.")
        print("The backend will use mock data instead of real AI-generated signals.")
        print("To use real AI-generated signals, update the OPENAI_API_KEY in the .env file.")
    else:
        print(f"\n✅ OpenAI API key is configured: {openai_key[:5]}...{openai_key[-4:]}")
    
    print("\n===== Backend Test Complete =====\n")
    print("To connect with the frontend:")
    print("1. Make sure the frontend is running")
    print("2. Ensure the frontend is configured to connect to http://localhost:8000")
    print("3. Open the frontend in your browser and test the trading signals")

if __name__ == "__main__":
    main()