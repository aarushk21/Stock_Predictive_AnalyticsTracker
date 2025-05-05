from sqlalchemy import Column, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Stock(BaseModel):
    __tablename__ = "stocks"

    symbol = Column(String, unique=True, index=True, nullable=False)
    company_name = Column(String)
    current_price = Column(Float)
    previous_close = Column(Float)
    market_cap = Column(Float)
    pe_ratio = Column(Float)
    dividend_yield = Column(Float)
    technical_indicators = Column(JSON)
    last_updated = Column(String)

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