# AI Trading Website

A real-time AI trading platform that analyzes market data, provides trading signals with confidence scores, and recommends stop-loss and take-profit levels.

## Features

- Real-time market data analysis
- Multiple trading strategies (FVG + Liquidity, RSI + MACD, Bollinger Breakout)
- Trading signals with confidence scores
- Stop-loss and take-profit recommendations
- Interactive price charts
- Market news integration
- Simulated trading panel

## Project Structure

```
AI_Trading_Website/
├── backend/
│   ├── src/
│   │   ├── main.py         # Main FastAPI application
│   │   └── strategies.py   # Trading strategies and indicators
│   └── .env                # Environment variables
├── frontend/
│   ├── public/             # Static files
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Next.js pages
│   │   └── styles/         # CSS styles
│   ├── next.config.js      # Next.js configuration
│   ├── package.json        # Frontend dependencies
│   ├── tailwind.config.js  # Tailwind CSS configuration
│   └── tsconfig.json       # TypeScript configuration
├── requirements.txt        # Backend dependencies
└── README.md              # Documentation
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

The backend `.env` file contains the following API keys:

- `BINANCE_API_KEY` and `BINANCE_API_SECRET`: For accessing Binance cryptocurrency data
- `ALPACA_API_KEY` and `ALPACA_API_SECRET`: For accessing Alpaca stock market data (optional)
- `NEWS_API_KEY`: For fetching market news from NewsAPI

For development purposes, the repository includes generated placeholder API keys. For production use, replace these with actual API keys from the respective services.

4. Start the backend server:

```bash
cd backend/src
uvicorn main:app --reload
```

The backend will be available at http://localhost:8000

### Frontend Setup

1. Install dependencies:

```bash
cd frontend
npm install
# or
yarn install
```

2. Start the development server:

```bash
npm run dev
# or
yarn dev
```

The frontend will be available at http://localhost:3000

## Trading Strategies

### FVG + Liquidity

This strategy identifies Fair Value Gaps (FVG) and liquidity zones to determine potential entry and exit points. It uses RSI and MACD as confirmation indicators.

### RSI + MACD

Combines Relative Strength Index (RSI) and Moving Average Convergence Divergence (MACD) to generate trading signals based on overbought/oversold conditions and momentum.

### Bollinger Breakout

Identifies breakouts from Bollinger Bands to determine potential trend continuations or reversals.

## Stop-Loss and Take-Profit Calculation

- **Stop-Loss**: Calculated based on recent price lows (for buy signals) or highs (for sell signals)
- **Take-Profit**: Calculated using the Average True Range (ATR) to set dynamic profit targets

## Disclaimer

This application is for educational purposes only. Trading involves risk, and past performance is not indicative of future results. Always do your own research before making investment decisions.

## License

MIT