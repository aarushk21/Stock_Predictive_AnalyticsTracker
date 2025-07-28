from sqlalchemy import Column, String, Float, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel

class Stock(BaseModel):
    __tablename__ = "stocks"

    symbol = Column(String, unique=True, index=True, nullable=False)
    company_name = Column(String)
    current_price = Column(Float)
    
    # Previous day data
    previous_open = Column(Float)
    previous_high = Column(Float)
    previous_low = Column(Float)
    previous_close = Column(Float)
    previous_volume = Column(Integer)
    previous_date = Column(String)
    
    # Current day data
    current_open = Column(Float)
    current_high = Column(Float)
    current_low = Column(Float)
    current_volume = Column(Integer)
    current_time = Column(String)
    
    # Fundamental data
    market_cap = Column(Float)
    pe_ratio = Column(Float)
    dividend_yield = Column(Float)
    technical_indicators = Column(JSON)
    last_updated = Column(String)
    
    # Prediction data
    predicted_price_7d = Column(Float)
    predicted_price_30d = Column(Float)
    prediction_confidence = Column(Float)
    prediction_trend = Column(String)  # bullish, bearish, neutral
    prediction_last_updated = Column(String)

class StockPrediction(BaseModel):
    __tablename__ = "stock_predictions"

    stock_id = Column(Integer, ForeignKey("stocks.id"))
    prediction_date = Column(String)
    predicted_price = Column(Float)
    confidence_score = Column(Float)
    prediction_type = Column(String)  # short_term, medium_term, long_term
    model_used = Column(String)
    prediction_metadata = Column(JSON)

    stock = relationship("Stock", back_populates="predictions") 