from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
import asyncio
import json
import os
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Import configuration
from config import *

# Import trading strategies
from strategies import (
    detect_fvg,
    check_liquidity_zone,
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands,
    analyze_trade_signal,
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
    strategy = params.get("strategy", "fvg_liquidity")
    
    try:
        while True:
            # Get market data
            klines = get_klines(symbol, interval)
            price = get_price(symbol)
            
            if price is None:
                price = 0.0
                
            # Analyze trading signals based on selected strategy
            signal, confidence = analyze_trade_signal(klines, strategy)
            
            # Calculate stop loss and take profit levels
            stop_loss = calculate_stop_loss(klines, signal, price)
            take_profit = calculate_take_profit(klines, signal, price)
            
            # Get latest news
            news = get_news(symbol.replace("USDT", ""))
            
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

# Function to get candlestick data
def get_klines(symbol: str, interval: str) -> List[Dict]:
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100'
    headers = {}
    if BINANCE_API_KEY:
        headers['X-MBX-APIKEY'] = BINANCE_API_KEY
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        klines = [{
            'timestamp': int(k[0]),
            'open': float(k[1]),
            'high': float(k[2]),
            'low': float(k[3]),
            'close': float(k[4]),
            'volume': float(k[5])
        } for k in data]
        return klines
    except Exception as e:
        print(f"Error fetching klines: {e}")
        return []

# Function to get current price
def get_price(symbol: str) -> Optional[float]:
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    headers = {}
    if BINANCE_API_KEY:
        headers['X-MBX-APIKEY'] = BINANCE_API_KEY
        
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data['price'])
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

# Function to get news
def get_news(coin: str) -> List[str]:
    # Use NEWS_API_KEY if available, otherwise fallback to CoinGecko
    if NEWS_API_KEY:
        try:
            # Use a proper news API with the key
            url = f"https://newsapi.org/v2/everything?q={coin}&apiKey={NEWS_API_KEY}&pageSize=5"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = data.get('articles', [])
            news_texts = []
            
            for article in articles[:5]:
                title = article.get('title', 'No title')
                source = article.get('source', {}).get('name', 'Unknown')
                news_texts.append(f"{title} ({source})")
                
            if not news_texts:
                return ["No recent news available."]
                
            return news_texts
        except Exception as e:
            print(f"Error fetching news from NewsAPI: {e}")
            # Fall back to CoinGecko if NewsAPI fails
    
    # Fallback to CoinGecko
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin.lower()}/status_updates"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        news_items = data.get('status_updates', [])
        news_texts = []
        
        for item in news_items[:5]:
            description = item.get('description', 'No description')
            project = item.get('project', {}).get('name', 'Unknown')
            news_texts.append(f"{description} ({project})")
            
        if not news_texts:
            return ["No recent news available."]
            
        return news_texts
    except Exception as e:
        print(f"Error fetching news from CoinGecko: {e}")
        return ["Unable to fetch news."]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)