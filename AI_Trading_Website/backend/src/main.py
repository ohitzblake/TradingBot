from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
import asyncio
import json
import os
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

# Import configuration
from config import *

# Optional: Import OpenAI for API calls
try:
    import openai
    OPENAI_AVAILABLE = True
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
except ImportError:
    OPENAI_AVAILABLE = False

# Import trading strategies for fallback
from strategies import (
    calculate_stop_loss,
    calculate_take_profit
)

app = FastAPI(title="AI Trading Website")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
@app.get("/")
async def get():
    return {"message": "AI Trading API is running"}

# WebSocket endpoint for real-time trading signals
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    params = websocket.query_params
    symbol = params.get("symbol", "BTCUSDT").upper()
    interval = params.get("interval", "1m")
    strategy = params.get("strategy", "ai_analysis")
    
    try:
        while True:
            # Get market data (now using mock data or OpenAI)
            price = get_price(symbol)
            
            if price is None:
                price = 0.0
                
            # Get trading signals using OpenAI
            signal, confidence = get_ai_trading_signal(symbol, strategy)
            
            # Calculate stop loss and take profit levels (using simplified approach)
            stop_loss = price * 0.95 if signal == "BUY" else price * 1.05
            take_profit = price * 1.1 if signal == "BUY" else price * 0.9
            
            # Get latest news using OpenAI
            news = get_ai_news(symbol.replace("USDT", ""))
            
            # Prepare data to send to client
            data = {
                "price": price,
                "signal": signal,
                "confidence": confidence,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "news": news
            }
            
            await websocket.send_json(data)
            await asyncio.sleep(5)  # Update every 5 seconds
            
    except WebSocketDisconnect:
        print(f"Client disconnected")
    except Exception as e:
        print(f"Error: {e}")

# Function to get mock or real price data
def get_price(symbol: str) -> Optional[float]:
    # If we're using mock data, generate a realistic price
    if USE_MOCK_DATA:
        # Base prices for common cryptocurrencies
        base_prices = {
            "BTCUSDT": 50000.0,
            "ETHUSDT": 3000.0,
            "BNBUSDT": 400.0,
            "ADAUSDT": 1.2,
            "DOGEUSDT": 0.25,
            "XRPUSDT": 0.75,
            "SOLUSDT": 100.0
        }
        
        # Get base price or use default
        base_price = base_prices.get(symbol, 100.0)
        
        # Add some random variation (±2%)
        variation = random.uniform(-0.02, 0.02)
        return base_price * (1 + variation)
    
    # Otherwise try to get real data
    try:
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data['price'])
    except Exception as e:
        print(f"Error fetching price: {e}")
        # Fall back to mock data if real API fails
        return 50000.0 if symbol == "BTCUSDT" else 3000.0

# Function to get AI-powered trading signals
def get_ai_trading_signal(symbol: str, strategy: str) -> Tuple[str, float]:
    # If OpenAI is available and configured, use it
    if OPENAI_AVAILABLE and OPENAI_API_KEY:
        try:
            # Create a prompt for the OpenAI API
            prompt = f"""Based on current market conditions for {symbol}, provide a trading signal.
            Format your response as a JSON object with two fields:
            1. 'signal': Either 'BUY', 'SELL', or 'HOLD'
            2. 'confidence': A number between 0 and 1 representing your confidence level
            
            Only respond with the JSON object, nothing else."""
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a trading assistant that provides signals based on market analysis."},
                          {"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            # Parse the response
            try:
                content = response.choices[0].message.content.strip()
                data = json.loads(content)
                signal = data.get('signal', 'HOLD')
                confidence = float(data.get('confidence', 0.5))
                return signal, confidence
            except (json.JSONDecodeError, ValueError, AttributeError) as e:
                print(f"Error parsing OpenAI response: {e}")
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
    
    # Fall back to random signals if OpenAI is not available
    signals = ["BUY", "SELL", "HOLD"]
    weights = [0.3, 0.3, 0.4]  # Slightly biased toward HOLD
    signal = random.choices(signals, weights=weights)[0]
    confidence = random.uniform(0.5, 0.9)
    return signal, confidence

# Function to get AI-generated news
def get_ai_news(coin: str) -> List[str]:
    # If OpenAI is available and configured, use it
    if OPENAI_AVAILABLE and OPENAI_API_KEY:
        try:
            # Create a prompt for the OpenAI API
            prompt = f"""Generate 3 recent and realistic sounding news headlines about {coin} cryptocurrency.
            Each headline should be informative and include a source name in parentheses at the end.
            Format your response as a JSON array of strings.
            Example: ["Bitcoin reaches new all-time high above $70,000 (CoinDesk)", "..."]
            
            Only respond with the JSON array, nothing else."""
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a financial news assistant that provides the latest cryptocurrency news."},
                          {"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            # Parse the response
            try:
                content = response.choices[0].message.content.strip()
                news_texts = json.loads(content)
                if isinstance(news_texts, list) and len(news_texts) > 0:
                    return news_texts
            except (json.JSONDecodeError, ValueError, AttributeError) as e:
                print(f"Error parsing OpenAI news response: {e}")
        except Exception as e:
            print(f"Error calling OpenAI API for news: {e}")
    
    # Fall back to mock news if OpenAI is not available
    current_date = datetime.now().strftime("%b %d")
    mock_news = [
        f"{coin} shows promising growth amid market volatility ({current_date}) (CryptoNews)",
        f"Analysts predict bullish trend for {coin} in coming weeks (MarketWatch)",
        f"New {coin} partnership announced with major tech company (CoinTelegraph)",
        f"{coin} community grows as adoption increases worldwide (CryptoDaily)",
        f"Regulatory clarity provides boost to {coin} price (Bloomberg)"
    ]
    
    # Return 3-5 random news items
    return random.sample(mock_news, min(3, len(mock_news)))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)