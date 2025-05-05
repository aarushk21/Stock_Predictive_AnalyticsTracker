import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import axios from 'axios';

interface StockState {
  currentStock: any;
  historicalData: any;
  news: any;
  loading: boolean;
  error: string | null;
}

const initialState: StockState = {
  currentStock: null,
  historicalData: null,
  news: null,
  loading: false,
  error: null,
};

export const fetchStockData = createAsyncThunk(
  'stock/fetchStockData',
  async (symbol: string) => {
    const response = await axios.get(`http://localhost:8000/api/v1/stocks/quote/${symbol}`);
    return response.data;
  }
);

export const fetchHistoricalData = createAsyncThunk(
  'stock/fetchHistoricalData',
  async (symbol: string) => {
    const response = await axios.get(`http://localhost:8000/api/v1/stocks/historical/${symbol}`);
    return response.data;
  }
);

export const fetchStockNews = createAsyncThunk(
  'stock/fetchStockNews',
  async (symbol: string) => {
    const response = await axios.get(`http://localhost:8000/api/v1/stocks/news/${symbol}`);
    return response.data;
  }
);

const stockSlice = createSlice({
  name: 'stock',
  initialState,
  reducers: {
    clearStockData: (state) => {
      state.currentStock = null;
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