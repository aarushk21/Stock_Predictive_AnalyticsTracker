import os
import requests
from typing import Dict, Any, List
from datetime import datetime, timedelta

class NewsService:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"

    async def get_market_news(
        self,
        query: str = "stock market",
        from_date: str = None,
        to_date: str = None,
        language: str = "en",
        sort_by: str = "publishedAt"
    ) -> Dict[str, Any]:
        """Get market news articles."""
        if not from_date:
            from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        if not to_date:
            to_date = datetime.now().strftime("%Y-%m-%d")

        params = {
            "q": query,
            "from": from_date,
            "to": to_date,
            "language": language,
            "sortBy": sort_by,
            "apiKey": self.api_key
        }
        
        response = requests.get(f"{self.base_url}/everything", params=params)
        return response.json()

    async def get_company_news(
        self,
        company_name: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get news specific to a company."""
        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        to_date = datetime.now().strftime("%Y-%m-%d")

        params = {
            "q": company_name,
            "from": from_date,
            "to": to_date,
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": self.api_key
        }
        
        response = requests.get(f"{self.base_url}/everything", params=params)
        return response.json()

    async def get_top_business_news(self) -> Dict[str, Any]:
        """Get top business news headlines."""
        params = {
            "category": "business",
            "language": "en",
            "apiKey": self.api_key
        }
        
        response = requests.get(f"{self.base_url}/top-headlines", params=params)
        return response.json()

    async def analyze_sentiment(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Basic sentiment analysis of news articles.
        This is a simple implementation that could be enhanced with more sophisticated NLP.
        """
        positive_words = {"up", "rise", "gain", "positive", "growth", "profit", "bullish"}
        negative_words = {"down", "fall", "loss", "negative", "decline", "bearish"}
        
        sentiment_scores = []
        
        for article in articles:
            title = article.get("title", "").lower()
            description = article.get("description", "").lower()
            content = f"{title} {description}"
            
            positive_count = sum(1 for word in positive_words if word in content)
            negative_count = sum(1 for word in negative_words if word in content)
            
            if positive_count > negative_count:
                sentiment = "positive"
            elif negative_count > positive_count:
                sentiment = "negative"
            else:
                sentiment = "neutral"
                
            sentiment_scores.append({
                "title": article.get("title"),
                "sentiment": sentiment,
                "score": positive_count - negative_count
            })
            
        return {
            "articles": sentiment_scores,
            "overall_sentiment": self._calculate_overall_sentiment(sentiment_scores)
        }
    
    def _calculate_overall_sentiment(self, sentiment_scores: List[Dict[str, Any]]) -> str:
        """Calculate overall sentiment from individual article sentiments."""
        positive_count = sum(1 for score in sentiment_scores if score["sentiment"] == "positive")
        negative_count = sum(1 for score in sentiment_scores if score["sentiment"] == "negative")
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        return "neutral" 