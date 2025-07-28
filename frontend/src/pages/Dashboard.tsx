import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  TextField,
  Button,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  LinearProgress,
  Alert,
  Divider,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  ShowChart,
  Analytics,
  Refresh,
  Visibility,
  VisibilityOff
} from '@mui/icons-material';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip as ChartTooltip,
  Legend,
} from 'chart.js';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store';
import {
  fetchComprehensiveStockData,
  fetchStockPredictions,
  fetchPredictionSummary,
  fetchStockNews
} from '../store/slices/stockSlice';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  ChartTooltip,
  Legend
);

const Dashboard: React.FC = () => {
  const dispatch = useDispatch();
  const { comprehensiveData, predictions, predictionSummary, news, loading, error } = useSelector(
    (state: RootState) => state.stock
  );

  const [searchQuery, setSearchQuery] = useState('AAPL');
  const [showPredictions, setShowPredictions] = useState(true);

  useEffect(() => {
    if (searchQuery) {
      handleSearch();
    }
  }, []);

  const handleSearch = () => {
    if (searchQuery) {
      dispatch(fetchComprehensiveStockData(searchQuery));
      dispatch(fetchStockPredictions({ symbol: searchQuery, days: 7 }));
      dispatch(fetchPredictionSummary(searchQuery));
      dispatch(fetchStockNews(searchQuery));
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  const formatPercentage = (value: number) => {
    return `${value > 0 ? '+' : ''}${value.toFixed(2)}%`;
  };

  const getPriceChangeColor = (change: number) => {
    return change >= 0 ? 'success' : 'error';
  };

  const renderStockOverview = () => {
    if (!comprehensiveData) return null;

    const currentData = comprehensiveData.current_data;
    const previousData = comprehensiveData.previous_day_data;
    const currentDayData = comprehensiveData.current_day_data;

    return (
      <Grid container spacing={3}>
        {/* Current Price Card */}
        <Grid item xs={12} md={4}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" color="primary" gutterBottom>
                Current Price
              </Typography>
              <Typography variant="h3" component="div">
                {formatCurrency(parseFloat(currentData?.['05. price'] || '0'))}
              </Typography>
              <Box display="flex" alignItems="center" mt={1}>
                <Chip
                  icon={parseFloat(currentData?.['09. change'] || '0') >= 0 ? <TrendingUp /> : <TrendingDown />}
                  label={formatPercentage(parseFloat(currentData?.['09. change'] || '0'))}
                  color={getPriceChangeColor(parseFloat(currentData?.['09. change'] || '0'))}
                  size="small"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Previous Day Data */}
        <Grid item xs={12} md={4}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" color="text.secondary" gutterBottom>
                Previous Day
              </Typography>
              <Grid container spacing={1}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">Open</Typography>
                  <Typography variant="h6">{formatCurrency(previousData?.open || 0)}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">Close</Typography>
                  <Typography variant="h6">{formatCurrency(previousData?.close || 0)}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">High</Typography>
                  <Typography variant="h6">{formatCurrency(previousData?.high || 0)}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">Low</Typography>
                  <Typography variant="h6">{formatCurrency(previousData?.low || 0)}</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Current Day Data */}
        <Grid item xs={12} md={4}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" color="text.secondary" gutterBottom>
                Current Day
              </Typography>
              <Grid container spacing={1}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">Open</Typography>
                  <Typography variant="h6">{formatCurrency(currentDayData?.open || 0)}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">Current</Typography>
                  <Typography variant="h6">{formatCurrency(currentDayData?.close || 0)}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">High</Typography>
                  <Typography variant="h6">{formatCurrency(currentDayData?.high || 0)}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">Low</Typography>
                  <Typography variant="h6">{formatCurrency(currentDayData?.low || 0)}</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  };

  const renderPredictions = () => {
    if (!predictionSummary || !showPredictions) return null;

    const summary = predictionSummary.prediction_summary;

    return (
      <Grid container spacing={3}>
        {/* Prediction Summary */}
        <Grid item xs={12} md={6}>
          <Card elevation={3}>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6" color="primary">
                  <Analytics sx={{ mr: 1 }} />
                  Price Predictions
                </Typography>
                <Tooltip title={showPredictions ? "Hide Predictions" : "Show Predictions"}>
                  <IconButton
                    size="small"
                    onClick={() => setShowPredictions(!showPredictions)}
                  >
                    {showPredictions ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </Tooltip>
              </Box>
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">Average Prediction</Typography>
                  <Typography variant="h5" color="primary">
                    {formatCurrency(summary?.average_prediction || 0)}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">Trend</Typography>
                  <Chip
                    label={summary?.trend || 'neutral'}
                    color={summary?.trend === 'bullish' ? 'success' : summary?.trend === 'bearish' ? 'error' : 'default'}
                    size="small"
                  />
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">Confidence</Typography>
                  <Box display="flex" alignItems="center">
                    <LinearProgress
                      variant="determinate"
                      value={summary?.confidence || 0}
                      sx={{ width: '60%', mr: 1 }}
                    />
                    <Typography variant="body2">{summary?.confidence || 0}%</Typography>
                  </Box>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">Trend Strength</Typography>
                  <Typography variant="body1">{summary?.trend_strength || 0}%</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Daily Predictions Table */}
        <Grid item xs={12} md={6}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" color="primary" gutterBottom>
                Daily Predictions
              </Typography>
              <TableContainer component={Paper} elevation={0}>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Date</TableCell>
                      <TableCell align="right">Predicted Price</TableCell>
                      <TableCell align="right">Confidence</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {predictionSummary.daily_predictions?.slice(0, 5).map((prediction: any, index: number) => (
                      <TableRow key={index}>
                        <TableCell>{prediction.date}</TableCell>
                        <TableCell align="right">
                          {formatCurrency(prediction.predicted_price)}
                        </TableCell>
                        <TableCell align="right">
                          <LinearProgress
                            variant="determinate"
                            value={prediction.confidence * 100}
                            sx={{ width: '60px', height: '8px' }}
                          />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  };

  const renderChart = () => {
    if (!comprehensiveData) return null;

    const chartData = {
      labels: ['Previous Open', 'Previous High', 'Previous Low', 'Previous Close', 'Current'],
      datasets: [
        {
          label: 'Stock Price',
          data: [
            comprehensiveData.previous_day_data?.open || 0,
            comprehensiveData.previous_day_data?.high || 0,
            comprehensiveData.previous_day_data?.low || 0,
            comprehensiveData.previous_day_data?.close || 0,
            parseFloat(comprehensiveData.current_data?.['05. price'] || '0')
          ],
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          tension: 0.1,
        },
      ],
    };

    const options = {
      responsive: true,
      plugins: {
        legend: {
          position: 'top' as const,
        },
        title: {
          display: true,
          text: 'Price Movement',
        },
      },
      scales: {
        y: {
          beginAtZero: false,
        },
      },
    };

    return (
      <Card elevation={3}>
        <CardContent>
          <Typography variant="h6" color="primary" gutterBottom>
            <ShowChart sx={{ mr: 1 }} />
            Price Chart
          </Typography>
          <Line data={chartData} options={options} />
        </CardContent>
      </Card>
    );
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Stock Analytics Dashboard
      </Typography>

      {/* Search Section */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box display="flex" gap={2} alignItems="center">
            <TextField
              fullWidth
              label="Search Stock Symbol"
              variant="outlined"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value.toUpperCase())}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
            <Button
              variant="contained"
              color="primary"
              onClick={handleSearch}
              disabled={loading}
              startIcon={<Refresh />}
            >
              {loading ? 'Loading...' : 'Search'}
            </Button>
          </Box>
        </CardContent>
      </Card>

      {/* Loading and Error States */}
      {loading && <LinearProgress sx={{ mb: 2 }} />}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Stock Overview */}
      {comprehensiveData && (
        <>
          {renderStockOverview()}
          <Box sx={{ my: 3 }}>
            <Divider />
          </Box>
          {renderPredictions()}
          <Box sx={{ my: 3 }}>
            <Divider />
          </Box>
          {renderChart()}
        </>
      )}

      {/* Empty State */}
      {!comprehensiveData && !loading && (
        <Card>
          <CardContent>
            <Typography variant="h6" color="text.secondary" align="center">
              Enter a stock symbol to view comprehensive analytics
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default Dashboard; 