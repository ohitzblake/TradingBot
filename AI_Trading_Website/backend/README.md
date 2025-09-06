# AI Trading Website Backend

## Overview
This backend provides trading signals and market data using OpenAI's API for analysis. It offers a simplified approach that doesn't require actual trading API keys.

## Setup Instructions

### 1. Environment Setup

1. Make sure you have the `.env` file in the backend directory with the following variables:
   ```
   # API Configuration
   API_PORT=8000
   API_HOST=0.0.0.0
   
   # OpenAI API Key
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Mock Data Configuration
   USE_MOCK_DATA=true
   
   # Frontend URL for CORS
   FRONTEND_URL=http://localhost:3000
   ```

2. Replace `your_openai_api_key_here` with your actual OpenAI API key if you want to use real AI-generated trading signals and news.
   - You can get an API key from [OpenAI's platform](https://platform.openai.com/api-keys)
   - If you don't have an OpenAI API key, keep `USE_MOCK_DATA=true` to use mock data

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Backend

```bash
python src/main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- **GET /** - Health check endpoint
- **WebSocket /ws/{symbol}** - Real-time trading signals for the specified symbol

## Features

- AI-powered trading signal generation
- AI-generated market news
- Real-time WebSocket communication
- Mock data support when OpenAI API is not available

## Deployment

When deploying to a service like Render:

1. Set the environment variables in the Render dashboard
2. Set the build command to install dependencies
3. Set the start command to `python src/main.py`

## Troubleshooting

If you encounter issues:

1. Ensure your OpenAI API key is valid if not using mock data
2. Check that the frontend URL in the `.env` file matches your frontend deployment
3. Verify that the required ports are not blocked by firewalls