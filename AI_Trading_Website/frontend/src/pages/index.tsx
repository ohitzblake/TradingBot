import React, { useState, useEffect, useRef } from 'react';
import Head from 'next/head';
import { createChart, ColorType } from 'lightweight-charts';
import { Box, Container, Grid, Typography, Paper, Select, MenuItem, FormControl, InputLabel, Button, CircularProgress } from '@mui/material';
import TradingPanel from '../components/TradingPanel';
import SignalDisplay from '../components/SignalDisplay';
import NewsPanel from '../components/NewsPanel';
import StrategySelector from '../components/StrategySelector';
import Header from '../components/Header';

const Home: React.FC = () => {
  const [symbol, setSymbol] = useState<string>('BTCUSDT');
  const [interval, setInterval] = useState<string>('1m');
  const [strategy, setStrategy] = useState<string>('fvg_liquidity');
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [tradingData, setTradingData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const ws = useRef<WebSocket | null>(null);

  // Connect to WebSocket
  const connectWebSocket = () => {
    setLoading(true);
    setError(null);

    if (ws.current) {
      ws.current.close();
    }

    try {
      const wsUrl = `ws://localhost:8000/ws?symbol=${symbol}&interval=${interval}&strategy=${strategy}`;
      ws.current = new WebSocket(wsUrl);

      ws.current.onopen = () => {
        setIsConnected(true);
        setLoading(false);
      };

      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setTradingData(data);
        updateChart(data);
      };

      ws.current.onclose = () => {
        setIsConnected(false);
      };

      ws.current.onerror = (error) => {
        setError('WebSocket connection error. Please try again.');
        setLoading(false);
        setIsConnected(false);
      };
    } catch (err) {
      setError('Failed to connect to trading server.');
      setLoading(false);
      setIsConnected(false);
    }
  };

  // Initialize chart
  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 400,
      layout: {
        background: { type: ColorType.Solid, color: '#1E1E1E' },
        textColor: '#DDD',
      },
      grid: {
        vertLines: { color: '#2B2B43' },
        horzLines: { color: '#2B2B43' },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
    });

    const candleSeries = chart.addCandlestickSeries();

    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      chart.remove();
      window.removeEventListener('resize', handleResize);
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  // Update chart with new data
  const updateChart = (data: any) => {
    // This would be implemented to update the chart with new price data
    // For now, this is a placeholder
  };

  return (
    <div>
      <Head>
        <title>AI Trading Platform</title>
        <meta name="description" content="Real-time AI trading platform with market analysis" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Grid container spacing={3}>
          {/* Market Selection */}
          <Grid item xs={12} md={12}>
            <Paper sx={{ p: 2, display: 'flex', flexDirection: 'row', gap: 2, alignItems: 'center' }}>
              <FormControl sx={{ minWidth: 120 }}>
                <InputLabel>Symbol</InputLabel>
                <Select
                  value={symbol}
                  label="Symbol"
                  onChange={(e) => setSymbol(e.target.value)}
                >
                  <MenuItem value="BTCUSDT">BTC/USDT</MenuItem>
                  <MenuItem value="ETHUSDT">ETH/USDT</MenuItem>
                  <MenuItem value="BNBUSDT">BNB/USDT</MenuItem>
                  <MenuItem value="ADAUSDT">ADA/USDT</MenuItem>
                  <MenuItem value="SOLUSDT">SOL/USDT</MenuItem>
                </Select>
              </FormControl>

              <FormControl sx={{ minWidth: 120 }}>
                <InputLabel>Timeframe</InputLabel>
                <Select
                  value={interval}
                  label="Timeframe"
                  onChange={(e) => setInterval(e.target.value)}
                >
                  <MenuItem value="1m">1m</MenuItem>
                  <MenuItem value="5m">5m</MenuItem>
                  <MenuItem value="15m">15m</MenuItem>
                  <MenuItem value="30m">30m</MenuItem>
                  <MenuItem value="1h">1h</MenuItem>
                  <MenuItem value="4h">4h</MenuItem>
                  <MenuItem value="1d">1d</MenuItem>
                </Select>
              </FormControl>

              <StrategySelector strategy={strategy} setStrategy={setStrategy} />

              <Button 
                variant="contained" 
                color="primary" 
                onClick={connectWebSocket}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : isConnected ? 'Reconnect' : 'Start Trading'}
              </Button>
            </Paper>
          </Grid>

          {/* Chart */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 450 }}>
              <Typography component="h2" variant="h6" color="primary" gutterBottom>
                Price Chart
              </Typography>
              <div ref={chartContainerRef} style={{ height: '100%', width: '100%' }} />
            </Paper>
          </Grid>

          {/* Trading Signals */}
          <Grid item xs={12} md={4}>
            <SignalDisplay tradingData={tradingData} />
          </Grid>

          {/* Trading Panel */}
          <Grid item xs={12} md={8}>
            <TradingPanel tradingData={tradingData} symbol={symbol} />
          </Grid>

          {/* News Panel */}
          <Grid item xs={12} md={4}>
            <NewsPanel news={tradingData?.news || []} />
          </Grid>
        </Grid>
      </Container>
    </div>
  );
};

export default Home;