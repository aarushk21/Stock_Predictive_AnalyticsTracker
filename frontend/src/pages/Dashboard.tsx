import React, { useEffect, useState } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Box,
} from '@mui/material';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import axios from 'axios';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [stockData, setStockData] = useState<any>(null);
  const [marketNews, setMarketNews] = useState<any>(null);

  useEffect(() => {
    // Fetch initial data
    fetchStockData('AAPL');
    fetchMarketNews();
  }, []);

  const fetchStockData = async (symbol: string) => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/stocks/quote/${symbol}`);
      setStockData(response.data);
    } catch (error) {
      console.error('Error fetching stock data:', error);
    }
  };

  const fetchMarketNews = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/stocks/news/AAPL');
      setMarketNews(response.data);
    } catch (error) {
      console.error('Error fetching market news:', error);
    }
  };

  const handleSearch = () => {
    if (searchQuery) {
      fetchStockData(searchQuery);
    }
  };

  const chartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Stock Price',
        data: [150, 155, 160, 158, 165, 170],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Market Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Search Section */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box display="flex" gap={2}>
                <TextField
                  fullWidth
                  label="Search Stock"
                  variant="outlined"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleSearch}
                >
                  Search
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Stock Overview */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Stock Overview
              </Typography>
              {stockData && (
                <Box>
                  <Typography variant="h4">
                    {stockData['Global Quote']?.['01. symbol']}
                  </Typography>
                  <Typography variant="h5" color="primary">
                    ${stockData['Global Quote']?.['05. price']}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Change: {stockData['Global Quote']?.['09. change']}%
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Market Trends */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Market Trends
              </Typography>
              <Line data={chartData} />
            </CardContent>
          </Card>
        </Grid>

        {/* Market News */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Latest Market News
              </Typography>
              {marketNews?.articles?.slice(0, 5).map((article: any, index: number) => (
                <Box key={index} mb={2}>
                  <Typography variant="subtitle1">
                    {article.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {article.description}
                  </Typography>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 