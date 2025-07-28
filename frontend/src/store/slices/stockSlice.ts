import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import axios from 'axios';

interface StockState {
  currentStock: any;
  comprehensiveData: any;
  predictions: any;
  predictionSummary: any;
  historicalData: any;
  news: any;
  loading: boolean;
  error: string | null;
}

const initialState: StockState = {
  currentStock: null,
  comprehensiveData: null,
  predictions: null,
  predictionSummary: null,
  historicalData: null,
  news: null,
  loading: false,
  error: null,
};

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1/stocks';

export const fetchStockData = createAsyncThunk(
  'stock/fetchStockData',
  async (symbol: string) => {
    const response = await axios.get(`${API_BASE_URL}/quote/${symbol}`);
    return response.data;
  }
);

export const fetchComprehensiveStockData = createAsyncThunk(
  'stock/fetchComprehensiveStockData',
  async (symbol: string) => {
    const response = await axios.get(`${API_BASE_URL}/comprehensive/${symbol}`);
    return response.data;
  }
);

export const fetchStockPredictions = createAsyncThunk(
  'stock/fetchStockPredictions',
  async ({ symbol, days }: { symbol: string; days: number }) => {
    const response = await axios.get(`${API_BASE_URL}/predictions/${symbol}?days=${days}`);
    return response.data;
  }
);

export const fetchPredictionSummary = createAsyncThunk(
  'stock/fetchPredictionSummary',
  async (symbol: string) => {
    const response = await axios.get(`${API_BASE_URL}/prediction-summary/${symbol}`);
    return response.data;
  }
);

export const fetchHistoricalData = createAsyncThunk(
  'stock/fetchHistoricalData',
  async (symbol: string) => {
    const response = await axios.get(`${API_BASE_URL}/historical/${symbol}`);
    return response.data;
  }
);

export const fetchStockNews = createAsyncThunk(
  'stock/fetchStockNews',
  async (symbol: string) => {
    const response = await axios.get(`${API_BASE_URL}/news/${symbol}`);
    return response.data;
  }
);

const stockSlice = createSlice({
  name: 'stock',
  initialState,
  reducers: {
    clearStockData: (state) => {
      state.currentStock = null;
      state.comprehensiveData = null;
      state.predictions = null;
      state.predictionSummary = null;
      state.historicalData = null;
      state.news = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Stock Data
      .addCase(fetchStockData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchStockData.fulfilled, (state, action: PayloadAction<any>) => {
        state.loading = false;
        state.currentStock = action.payload;
      })
      .addCase(fetchStockData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch stock data';
      })
      // Fetch Comprehensive Stock Data
      .addCase(fetchComprehensiveStockData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchComprehensiveStockData.fulfilled, (state, action: PayloadAction<any>) => {
        state.loading = false;
        state.comprehensiveData = action.payload;
      })
      .addCase(fetchComprehensiveStockData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch comprehensive stock data';
      })
      // Fetch Stock Predictions
      .addCase(fetchStockPredictions.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchStockPredictions.fulfilled, (state, action: PayloadAction<any>) => {
        state.loading = false;
        state.predictions = action.payload;
      })
      .addCase(fetchStockPredictions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch stock predictions';
      })
      // Fetch Prediction Summary
      .addCase(fetchPredictionSummary.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPredictionSummary.fulfilled, (state, action: PayloadAction<any>) => {
        state.loading = false;
        state.predictionSummary = action.payload;
      })
      .addCase(fetchPredictionSummary.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch prediction summary';
      })
      // Fetch Historical Data
      .addCase(fetchHistoricalData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchHistoricalData.fulfilled, (state, action: PayloadAction<any>) => {
        state.loading = false;
        state.historicalData = action.payload;
      })
      .addCase(fetchHistoricalData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch historical data';
      })
      // Fetch Stock News
      .addCase(fetchStockNews.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchStockNews.fulfilled, (state, action: PayloadAction<any>) => {
        state.loading = false;
        state.news = action.payload;
      })
      .addCase(fetchStockNews.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch stock news';
      });
  },
});

export const { clearStockData } = stockSlice.actions;
export default stockSlice.reducer; 