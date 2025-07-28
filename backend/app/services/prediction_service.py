import os
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import ta
import yfinance as yf

class PredictionService:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False

    async def prepare_features(self, symbol: str, days: int = 60) -> pd.DataFrame:
        """Prepare features for prediction model."""
        try:
            # Get historical data using yfinance for more reliable data
            ticker = yf.Ticker(symbol)
            hist_data = ticker.history(period=f"{days}d")
            
            if hist_data.empty:
                return pd.DataFrame()
            
            # Calculate technical indicators
            df = hist_data.copy()
            
            # Moving averages
            df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
            df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
            df['EMA_12'] = ta.trend.ema_indicator(df['Close'], window=12)
            df['EMA_26'] = ta.trend.ema_indicator(df['Close'], window=26)
            
            # MACD
            df['MACD'] = ta.trend.macd_diff(df['Close'])
            df['MACD_signal'] = ta.trend.macd_signal(df['Close'])
            
            # RSI
            df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
            
            # Bollinger Bands
            df['BB_upper'] = ta.volatility.bollinger_hband(df['Close'])
            df['BB_lower'] = ta.volatility.bollinger_lband(df['Close'])
            df['BB_middle'] = ta.volatility.bollinger_mavg(df['Close'])
            
            # Volume indicators
            df['Volume_SMA'] = ta.volume.volume_sma(df['Close'], df['Volume'])
            
            # Price changes
            df['Price_Change'] = df['Close'].pct_change()
            df['Price_Change_5'] = df['Close'].pct_change(periods=5)
            df['Price_Change_10'] = df['Close'].pct_change(periods=10)
            
            # Volatility
            df['Volatility'] = df['Price_Change'].rolling(window=20).std()
            
            # Remove NaN values
            df = df.dropna()
            
            return df
            
        except Exception as e:
            print(f"Error preparing features: {e}")
            return pd.DataFrame()

    async def get_demo_predictions(self, symbol: str, days: int = 7) -> Dict[str, Any]:
        """Get demo predictions for testing without API keys."""
        current_price = 150.0  # Demo current price
        
        # Generate realistic demo predictions
        predictions = []
        base_price = current_price
        
        for day in range(1, days + 1):
            # Simulate realistic price movements
            change_pct = np.random.normal(0.02, 0.03)  # 2% mean, 3% std
            predicted_price = base_price * (1 + change_pct)
            base_price = predicted_price
            
            prediction_date = datetime.now() + timedelta(days=day)
            confidence = max(0.3, min(0.9, 0.7 + np.random.normal(0, 0.1)))
            
            predictions.append({
                "date": prediction_date.strftime("%Y-%m-%d"),
                "predicted_price": round(predicted_price, 2),
                "confidence": confidence
            })
        
        return {
            "symbol": symbol,
            "current_price": current_price,
            "predictions": predictions,
            "model_accuracy": 0.75,
            "demo_mode": True
        }

    async def get_demo_prediction_summary(self, symbol: str) -> Dict[str, Any]:
        """Get demo prediction summary for testing."""
        demo_predictions = await self.get_demo_predictions(symbol, 7)
        predictions = demo_predictions["predictions"]
        current_price = demo_predictions["current_price"]
        
        # Calculate summary statistics
        predicted_prices = [p["predicted_price"] for p in predictions]
        avg_prediction = np.mean(predicted_prices)
        max_prediction = max(predicted_prices)
        min_prediction = min(predicted_prices)
        
        # Determine trend
        price_trend = "bullish" if avg_prediction > current_price else "bearish"
        trend_strength = abs(avg_prediction - current_price) / current_price
        
        # Calculate confidence
        avg_confidence = np.mean([p["confidence"] for p in predictions])
        
        return {
            "symbol": symbol,
            "current_price": current_price,
            "prediction_summary": {
                "average_prediction": round(avg_prediction, 2),
                "max_prediction": round(max_prediction, 2),
                "min_prediction": round(min_prediction, 2),
                "trend": price_trend,
                "trend_strength": round(trend_strength * 100, 2),
                "confidence": round(avg_confidence * 100, 2)
            },
            "daily_predictions": predictions,
            "model_accuracy": 0.75,
            "demo_mode": True
        }

    async def train_model(self, symbol: str) -> Dict[str, Any]:
        """Train the prediction model for a specific stock."""
        try:
            # Check if we have API keys for real data
            if not os.getenv("ALPHA_VANTAGE_API_KEY") or os.getenv("ALPHA_VANTAGE_API_KEY") == "demo_key":
                return {"error": "API key required for real predictions. Using demo mode."}
            
            # Prepare features
            df = await self.prepare_features(symbol)
            
            if df.empty:
                return {"error": "No data available for training"}
            
            # Define features (excluding target variable)
            feature_columns = [
                'Open', 'High', 'Low', 'Close', 'Volume',
                'SMA_20', 'SMA_50', 'EMA_12', 'EMA_26',
                'MACD', 'MACD_signal', 'RSI',
                'BB_upper', 'BB_lower', 'BB_middle',
                'Volume_SMA', 'Price_Change', 'Price_Change_5',
                'Price_Change_10', 'Volatility'
            ]
            
            # Create target variable (next day's close price)
            df['Target'] = df['Close'].shift(-1)
            
            # Remove last row (no target) and first few rows (NaN from indicators)
            df = df.dropna()
            
            if len(df) < 30:  # Need sufficient data
                return {"error": "Insufficient data for training"}
            
            # Prepare X and y
            X = df[feature_columns].values
            y = df['Target'].values
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            train_score = self.model.score(X_train_scaled, y_train)
            test_score = self.model.score(X_test_scaled, y_test)
            
            self.is_trained = True
            
            return {
                "success": True,
                "train_score": train_score,
                "test_score": test_score,
                "model_info": f"RandomForest with {len(feature_columns)} features"
            }
            
        except Exception as e:
            return {"error": f"Training failed: {str(e)}"}

    async def predict_future_prices(self, symbol: str, days_ahead: int = 7) -> Dict[str, Any]:
        """Predict future stock prices."""
        try:
            # Check if we have API keys for real data
            if not os.getenv("ALPHA_VANTAGE_API_KEY") or os.getenv("ALPHA_VANTAGE_API_KEY") == "demo_key":
                return await self.get_demo_predictions(symbol, days_ahead)
            
            if not self.is_trained:
                # Train model first
                train_result = await self.train_model(symbol)
                if "error" in train_result:
                    return train_result
            
            # Get latest data for prediction
            df = await self.prepare_features(symbol)
            
            if df.empty:
                return {"error": "No data available for prediction"}
            
            # Get the most recent data point
            latest_data = df.iloc[-1]
            
            # Prepare features for prediction
            feature_columns = [
                'Open', 'High', 'Low', 'Close', 'Volume',
                'SMA_20', 'SMA_50', 'EMA_12', 'EMA_26',
                'MACD', 'MACD_signal', 'RSI',
                'BB_upper', 'BB_lower', 'BB_middle',
                'Volume_SMA', 'Price_Change', 'Price_Change_5',
                'Price_Change_10', 'Volatility'
            ]
            
            predictions = []
            current_data = latest_data[feature_columns].values.reshape(1, -1)
            
            for day in range(1, days_ahead + 1):
                # Scale the current data
                current_scaled = self.scaler.transform(current_data)
                
                # Make prediction
                predicted_price = self.model.predict(current_scaled)[0]
                
                # Add prediction to list
                prediction_date = datetime.now() + timedelta(days=day)
                predictions.append({
                    "date": prediction_date.strftime("%Y-%m-%d"),
                    "predicted_price": round(predicted_price, 2),
                    "confidence": self._calculate_confidence(predicted_price, latest_data['Close'])
                })
                
                # Update current data for next prediction (simplified approach)
                # In a more sophisticated model, you'd update all features
                current_data[0][3] = predicted_price  # Update Close price
            
            return {
                "symbol": symbol,
                "current_price": latest_data['Close'],
                "predictions": predictions,
                "model_accuracy": self.model.score(
                    self.scaler.transform(df[feature_columns].values),
                    df['Close'].values
                ) if 'Target' in df.columns else None
            }
            
        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}

    def _calculate_confidence(self, predicted_price: float, current_price: float) -> float:
        """Calculate confidence score based on prediction stability."""
        price_change_pct = abs(predicted_price - current_price) / current_price
        
        # Higher confidence for smaller price changes (more stable predictions)
        if price_change_pct < 0.05:  # Less than 5% change
            return 0.9
        elif price_change_pct < 0.10:  # Less than 10% change
            return 0.7
        elif price_change_pct < 0.20:  # Less than 20% change
            return 0.5
        else:
            return 0.3

    async def get_prediction_summary(self, symbol: str) -> Dict[str, Any]:
        """Get a summary of predictions with key insights."""
        try:
            # Check if we have API keys for real data
            if not os.getenv("ALPHA_VANTAGE_API_KEY") or os.getenv("ALPHA_VANTAGE_API_KEY") == "demo_key":
                return await self.get_demo_prediction_summary(symbol)
            
            prediction_result = await self.predict_future_prices(symbol, 7)
            
            if "error" in prediction_result:
                return prediction_result
            
            predictions = prediction_result["predictions"]
            current_price = prediction_result["current_price"]
            
            if not predictions:
                return {"error": "No predictions available"}
            
            # Calculate summary statistics
            predicted_prices = [p["predicted_price"] for p in predictions]
            avg_prediction = np.mean(predicted_prices)
            max_prediction = max(predicted_prices)
            min_prediction = min(predicted_prices)
            
            # Determine trend
            price_trend = "bullish" if avg_prediction > current_price else "bearish"
            trend_strength = abs(avg_prediction - current_price) / current_price
            
            # Calculate confidence
            avg_confidence = np.mean([p["confidence"] for p in predictions])
            
            return {
                "symbol": symbol,
                "current_price": current_price,
                "prediction_summary": {
                    "average_prediction": round(avg_prediction, 2),
                    "max_prediction": round(max_prediction, 2),
                    "min_prediction": round(min_prediction, 2),
                    "trend": price_trend,
                    "trend_strength": round(trend_strength * 100, 2),
                    "confidence": round(avg_confidence * 100, 2)
                },
                "daily_predictions": predictions,
                "model_accuracy": prediction_result.get("model_accuracy")
            }
            
        except Exception as e:
            return {"error": f"Summary generation failed: {str(e)}"} 