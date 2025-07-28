from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from app.services.alpha_vantage_service import AlphaVantageService
from app.services.news_service import NewsService
from app.services.prediction_service import PredictionService

router = APIRouter()
alpha_vantage_service = AlphaVantageService()
news_service = NewsService()
prediction_service = PredictionService()

@router.get("/quote/{symbol}")
async def get_stock_quote(symbol: str) -> Dict[str, Any]:
    """Get real-time stock quote data."""
    try:
        data = await alpha_vantage_service.get_stock_quote(symbol)
        if "Error Message" in data:
            raise HTTPException(status_code=400, detail=data["Error Message"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/comprehensive/{symbol}")
async def get_comprehensive_stock_data(symbol: str) -> Dict[str, Any]:
    """Get comprehensive stock data including previous day OHLC and current day data."""
    try:
        data = await alpha_vantage_service.get_comprehensive_stock_data(symbol)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predictions/{symbol}")
async def get_stock_predictions(symbol: str, days: int = 7) -> Dict[str, Any]:
    """Get future stock price predictions."""
    try:
        if days > 30:
            raise HTTPException(status_code=400, detail="Maximum prediction days is 30")
        
        data = await prediction_service.predict_future_prices(symbol, days)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/prediction-summary/{symbol}")
async def get_prediction_summary(symbol: str) -> Dict[str, Any]:
    """Get a summary of stock predictions with key insights."""
    try:
        data = await prediction_service.get_prediction_summary(symbol)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/overview/{symbol}")
async def get_company_overview(symbol: str) -> Dict[str, Any]:
    """Get company overview and fundamental data."""
    try:
        data = await alpha_vantage_service.get_company_overview(symbol)
        if not data:
            raise HTTPException(status_code=404, detail="Company data not found")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/technical/{symbol}")
async def get_technical_indicators(
    symbol: str,
    indicator: str = "SMA",
    interval: str = "daily",
    time_period: int = 20
) -> Dict[str, Any]:
    """Get technical indicators for a stock."""
    try:
        data = await alpha_vantage_service.get_technical_indicators(
            symbol, indicator, interval, time_period
        )
        if "Error Message" in data:
            raise HTTPException(status_code=400, detail=data["Error Message"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/historical/{symbol}")
async def get_historical_data(
    symbol: str,
    interval: str = "daily",
    output_size: str = "compact"
) -> Dict[str, Any]:
    """Get historical price data."""
    try:
        data = await alpha_vantage_service.get_historical_data(symbol, interval, output_size)
        if "Error Message" in data:
            raise HTTPException(status_code=400, detail=data["Error Message"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_stocks(keywords: str) -> Dict[str, Any]:
    """Search for stocks by keywords."""
    try:
        data = await alpha_vantage_service.search_stocks(keywords)
        if "Error Message" in data:
            raise HTTPException(status_code=400, detail=data["Error Message"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news/{symbol}")
async def get_stock_news(symbol: str, days: int = 7) -> Dict[str, Any]:
    """Get news and sentiment analysis for a stock."""
    try:
        # Get company overview to get company name
        overview = await alpha_vantage_service.get_company_overview(symbol)
        company_name = overview.get("Name", symbol)
        
        # Get news articles
        news_data = await news_service.get_company_news(company_name, days)
        
        # Analyze sentiment
        if "articles" in news_data:
            sentiment_analysis = await news_service.analyze_sentiment(news_data["articles"])
            news_data["sentiment_analysis"] = sentiment_analysis
            
        return news_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 