import React from 'react';
import { Paper, Typography, Box, Chip, LinearProgress } from '@mui/material';
import { TrendingUp, TrendingDown, TrendingFlat } from '@mui/icons-material';

interface SignalDisplayProps {
  tradingData: {
    price: number;
    signal: string;
    confidence: number;
    stop_loss: number;
    take_profit: number;
  } | null;
}

const SignalDisplay: React.FC<SignalDisplayProps> = ({ tradingData }) => {
  if (!tradingData) {
    return (
      <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: '100%' }}>
        <Typography component="h2" variant="h6" color="primary" gutterBottom>
          Trading Signals
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
          <Typography variant="body1" color="text.secondary">
            Connect to start receiving signals
          </Typography>
        </Box>
      </Paper>
    );
  }

  const { price, signal, confidence, stop_loss, take_profit } = tradingData;
  const confidencePercent = confidence * 100;

  const getSignalColor = () => {
    switch (signal) {
      case 'BUY':
        return 'success';
      case 'SELL':
        return 'error';
      default:
        return 'warning';
    }
  };

  const getSignalIcon = () => {
    switch (signal) {
      case 'BUY':
        return <TrendingUp />;
      case 'SELL':
        return <TrendingDown />;
      default:
        return <TrendingFlat />;
    }
  };

  return (
    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: '100%' }}>
      <Typography component="h2" variant="h6" color="primary" gutterBottom>
        Trading Signals
      </Typography>
      
      <Box sx={{ mb: 2 }}>
        <Typography variant="body2" color="text.secondary">
          Current Price
        </Typography>
        <Typography variant="h4">
          ${price.toFixed(2)}
        </Typography>
      </Box>

      <Box sx={{ mb: 2 }}>
        <Typography variant="body2" color="text.secondary">
          Signal
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
          <Chip 
            icon={getSignalIcon()} 
            label={signal} 
            color={getSignalColor() as any} 
            variant="outlined" 
            sx={{ fontWeight: 'bold', fontSize: '1.1rem' }}
          />
        </Box>
      </Box>

      <Box sx={{ mb: 2 }}>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Confidence
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Box sx={{ width: '100%', mr: 1 }}>
            <LinearProgress 
              variant="determinate" 
              value={confidencePercent} 
              color={confidencePercent > 80 ? 'success' : confidencePercent > 50 ? 'primary' : 'warning'}
              sx={{ height: 10, borderRadius: 5 }}
            />
          </Box>
          <Box>
            <Typography variant="body2" color="text.secondary">
              {confidencePercent.toFixed(1)}%
            </Typography>
          </Box>
        </Box>
      </Box>

      {signal !== 'HOLD' && (
        <>
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Stop Loss
            </Typography>
            <Typography variant="h6" color="error">
              ${stop_loss.toFixed(2)}
            </Typography>
          </Box>

          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Take Profit
            </Typography>
            <Typography variant="h6" color="success">
              ${take_profit.toFixed(2)}
            </Typography>
          </Box>
        </>
      )}
    </Paper>
  );
};

export default SignalDisplay;