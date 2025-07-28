import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class AlphaVantageService:
    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.base_url = "https://www.alphavantage.co/query"

    async def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time stock quote data."""
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()

    async def get_comprehensive_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive stock data including previous day OHLC and current day data."""
        try:
            # Get real-time quote
            quote_data = await self.get_stock_quote(symbol)
            
            # Get daily time series for previous day data
            daily_data = await self.get_historical_data(symbol, "daily", "compact")
            
            # Get intraday data for current day
            intraday_data = await self.get_intraday_data(symbol)
            
            # Combine all data
            comprehensive_data = {
                "symbol": symbol,
                "current_data": quote_data.get("Global Quote", {}),
                "previous_day_data": {},
                "current_day_data": {},
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Extract previous day data from daily time series
            if "Time Series (Daily)" in daily_data:
                daily_series = daily_data["Time Series (Daily)"]
                dates = sorted(daily_series.keys(), reverse=True)
                if len(dates) >= 2:  # We need at least 2 days of data
                    previous_day = dates[1]  # Most recent is today, second is previous day
                    previous_data = daily_series[previous_day]
                    comprehensive_data["previous_day_data"] = {
                        "date": previous_day,
                        "open": float(previous_data.get("1. open", 0)),
                        "high": float(previous_data.get("2. high", 0)),
                        "low": float(previous_data.get("3. low", 0)),
                        "close": float(previous_data.get("4. close", 0)),
                        "volume": int(previous_data.get("5. volume", 0))
                    }
            
            # Extract current day data from intraday
            if "Time Series (1min)" in intraday_data:
                intraday_series = intraday_data["Time Series (1min)"]
                current_times = sorted(intraday_series.keys(), reverse=True)
                if current_times:
                    latest_time = current_times[0]
                    current_data = intraday_series[latest_time]
                    comprehensive_data["current_day_data"] = {
                        "time": latest_time,
                        "open": float(current_data.get("1. open", 0)),
                        "high": float(current_data.get("2. high", 0)),
                        "low": float(current_data.get("3. low", 0)),
                        "close": float(current_data.get("4. close", 0)),
                        "volume": int(current_data.get("5. volume", 0))
                    }
            
            return comprehensive_data
            
        except Exception as e:
            return {"error": str(e)}

    async def get_intraday_data(
        self, 
        symbol: str, 
        interval: str = "1min",
        output_size: str = "compact"
    ) -> Dict[str, Any]:
        """Get intraday price data."""
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "outputsize": output_size,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()

    async def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """Get company overview and fundamental data."""
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()

    async def get_technical_indicators(
        self, 
        symbol: str, 
        indicator: str = "SMA",
        interval: str = "daily",
        time_period: int = 20
    ) -> Dict[str, Any]:
        """Get technical indicators for a stock."""
        params = {
            "function": indicator,
            "symbol": symbol,
            "interval": interval,
            "time_period": time_period,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()

    async def get_historical_data(
        self, 
        symbol: str, 
        interval: str = "daily",
        output_size: str = "compact"
    ) -> Dict[str, Any]:
        """Get historical price data."""
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": output_size,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()

    async def search_stocks(self, keywords: str) -> Dict[str, Any]:
        """Search for stocks by keywords."""
        params = {
            "function": "SYMBOL_SEARCH",
            "keywords": keywords,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json() 