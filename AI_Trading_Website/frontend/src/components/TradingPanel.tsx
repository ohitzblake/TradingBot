import React, { useState } from 'react';
import { Paper, Typography, Box, Button, TextField, Grid, Divider, Alert } from '@mui/material';

interface TradingPanelProps {
  tradingData: {
    price: number;
    signal: string;
    confidence: number;
    stop_loss: number;
    take_profit: number;
  } | null;
  symbol: string;
}

const TradingPanel: React.FC<TradingPanelProps> = ({ tradingData, symbol }) => {
  const [amount, setAmount] = useState<string>('');
  const [leverage, setLeverage] = useState<string>('1');
  const [orderPlaced, setOrderPlaced] = useState<boolean>(false);
  const [orderError, setOrderError] = useState<string | null>(null);

  if (!tradingData) {
    return (
      <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
        <Typography component="h2" variant="h6" color="primary" gutterBottom>
          Trading Panel
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Connect to start trading
        </Typography>
      </Paper>
    );
  }

  const { price, signal, confidence, stop_loss, take_profit } = tradingData;

  const handleAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value === '' || /^\d+(\.\d{0,2})?$/.test(value)) {
      setAmount(value);
    }
  };

  const handleLeverageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value === '' || (/^\d+$/.test(value) && parseInt(value) <= 100)) {
      setLeverage(value);
    }
  };

  const calculatePotentialProfit = () => {
    if (!amount || !tradingData || signal === 'HOLD') return 0;
    
    const amountValue = parseFloat(amount);
    const leverageValue = parseInt(leverage) || 1;
    
    if (signal === 'BUY') {
      return ((take_profit - price) / price) * amountValue * leverageValue;
    } else if (signal === 'SELL') {
      return ((price - take_profit) / price) * amountValue * leverageValue;
    }
    
    return 0;
  };

  const calculatePotentialLoss = () => {
    if (!amount || !tradingData || signal === 'HOLD') return 0;
    
    const amountValue = parseFloat(amount);
    const leverageValue = parseInt(leverage) || 1;
    
    if (signal === 'BUY') {
      return ((price - stop_loss) / price) * amountValue * leverageValue;
    } else if (signal === 'SELL') {
      return ((stop_loss - price) / price) * amountValue * leverageValue;
    }
    
    return 0;
  };

  const handlePlaceOrder = () => {
    // This would connect to a real trading API in a production environment
    // For now, we'll just simulate order placement
    if (!amount || parseFloat(amount) <= 0) {
      setOrderError('Please enter a valid amount');
      return;
    }
    
    setOrderPlaced(true);
    setOrderError(null);
    
    // Reset after 3 seconds
    setTimeout(() => {
      setOrderPlaced(false);
      setAmount('');
    }, 3000);
  };

  const potentialProfit = calculatePotentialProfit();
  const potentialLoss = calculatePotentialLoss();
  const riskRewardRatio = potentialLoss > 0 ? (potentialProfit / potentialLoss).toFixed(2) : 'N/A';

  return (
    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
      <Typography component="h2" variant="h6" color="primary" gutterBottom>
        Trading Panel - {symbol}
      </Typography>
      
      {orderPlaced && (
        <Alert severity="success" sx={{ mb: 2 }}>
          Order placed successfully!
        </Alert>
      )}
      
      {orderError && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {orderError}
        </Alert>
      )}
      
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Current Signal
            </Typography>
            <Typography variant="h6" color={signal === 'BUY' ? 'success.main' : signal === 'SELL' ? 'error.main' : 'text.secondary'}>
              {signal}
            </Typography>
          </Box>
          
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Confidence
            </Typography>
            <Typography variant="h6">
              {(confidence * 100).toFixed(1)}%
            </Typography>
          </Box>
          
          {signal !== 'HOLD' && (
            <>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Stop Loss
                </Typography>
                <Typography variant="h6" color="error.main">
                  ${stop_loss.toFixed(2)}
                </Typography>
              </Box>
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Take Profit
                </Typography>
                <Typography variant="h6" color="success.main">
                  ${take_profit.toFixed(2)}
                </Typography>
              </Box>
            </>
          )}
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Box sx={{ mb: 2 }}>
            <TextField
              label="Amount (USD)"
              variant="outlined"
              fullWidth
              value={amount}
              onChange={handleAmountChange}
              disabled={signal === 'HOLD'}
            />
          </Box>
          
          <Box sx={{ mb: 2 }}>
            <TextField
              label="Leverage"
              variant="outlined"
              fullWidth
              value={leverage}
              onChange={handleLeverageChange}
              disabled={signal === 'HOLD'}
            />
          </Box>
          
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Potential Profit
            </Typography>
            <Typography variant="h6" color="success.main">
              ${potentialProfit.toFixed(2)}
            </Typography>
          </Box>
          
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Potential Loss
            </Typography>
            <Typography variant="h6" color="error.main">
              ${potentialLoss.toFixed(2)}
            </Typography>
          </Box>
          
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Risk/Reward Ratio
            </Typography>
            <Typography variant="h6">
              {riskRewardRatio}
            </Typography>
          </Box>
        </Grid>
      </Grid>
      
      <Divider sx={{ my: 2 }} />
      
      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Button 
          variant="contained" 
          color="success" 
          disabled={signal !== 'BUY' || !amount || parseFloat(amount) <= 0}
          onClick={handlePlaceOrder}
          sx={{ minWidth: 120 }}
        >
          Buy / Long
        </Button>
        
        <Button 
          variant="contained" 
          color="error" 
          disabled={signal !== 'SELL' || !amount || parseFloat(amount) <= 0}
          onClick={handlePlaceOrder}
          sx={{ minWidth: 120 }}
        >
          Sell / Short
        </Button>
      </Box>
    </Paper>
  );
};

export default TradingPanel;