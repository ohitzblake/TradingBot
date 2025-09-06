import React from 'react';
import { Paper, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';

interface NewsPanelProps {
  news: string[];
}

const NewsPanel: React.FC<NewsPanelProps> = ({ news }) => {
  return (
    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: '100%' }}>
      <Typography component="h2" variant="h6" color="primary" gutterBottom>
        Market News
      </Typography>
      
      {news.length === 0 ? (
        <Typography variant="body1" color="text.secondary">
          No news available
        </Typography>
      ) : (
        <List sx={{ width: '100%', overflow: 'auto' }}>
          {news.map((item, index) => (
            <React.Fragment key={index}>
              <ListItem alignItems="flex-start">
                <ListItemText
                  primary={item}
                />
              </ListItem>
              {index < news.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      )}
    </Paper>
  );
};

export default NewsPanel;