import React from 'react';
import { FormControl, InputLabel, Select, MenuItem, SelectChangeEvent } from '@mui/material';

interface StrategySelectorProps {
  strategy: string;
  setStrategy: (strategy: string) => void;
}

const StrategySelector: React.FC<StrategySelectorProps> = ({ strategy, setStrategy }) => {
  const handleChange = (event: SelectChangeEvent) => {
    setStrategy(event.target.value);
  };

  return (
    <FormControl sx={{ minWidth: 200 }}>
      <InputLabel>Trading Strategy</InputLabel>
      <Select
        value={strategy}
        label="Trading Strategy"
        onChange={handleChange}
      >
        <MenuItem value="fvg_liquidity">FVG + Liquidity</MenuItem>
        <MenuItem value="rsi_macd">RSI + MACD</MenuItem>
        <MenuItem value="bollinger_breakout">Bollinger Breakout</MenuItem>
      </Select>
    </FormControl>
  );
};

export default StrategySelector;