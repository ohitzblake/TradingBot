import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { TrendingUp } from '@mui/icons-material';

const Header: React.FC = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Box display="flex" alignItems="center">
          <TrendingUp sx={{ mr: 1 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            AI Trading Platform
          </Typography>
        </Box>
        <Box sx={{ flexGrow: 1 }} />
        <Button color="inherit">Dashboard</Button>
        <Button color="inherit">Markets</Button>
        <Button color="inherit">Settings</Button>
      </Toolbar>
    </AppBar>
  );
};

export default Header;