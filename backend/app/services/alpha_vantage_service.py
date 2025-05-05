import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime

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