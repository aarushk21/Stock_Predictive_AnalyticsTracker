# Stock Predictive Analytics Tracker

A professional-grade stock market analysis and prediction platform that combines real-time market data, technical analysis, and machine learning to provide comprehensive stock insights and predictions.

## 🚀 New Features Added

### Enhanced Stock Data
- **Previous Day OHLC Data**: Open, High, Low, Close prices from the previous trading day
- **Current Day Data**: Real-time Open, High, Low, Current prices for today
- **Comprehensive Analytics**: Combined view of historical and current market performance

### AI-Powered Predictions
- **7-Day Price Predictions**: Machine learning-based forecasts for the next week
- **Prediction Confidence**: Confidence scores for each prediction
- **Trend Analysis**: Bullish/Bearish trend identification with strength indicators
- **Technical Indicators**: RSI, MACD, Bollinger Bands, Moving Averages

### Professional UI
- **Modern Dashboard**: Clean, responsive interface with Material-UI components
- **Interactive Charts**: Real-time price movement visualization
- **Prediction Tables**: Detailed daily prediction breakdown
- **Loading States**: Professional loading indicators and error handling

## Features

- 📈 **Real-time stock data** tracking and visualization
- 🤖 **Machine learning-based** price predictions
- 📊 **Technical analysis** indicators and patterns
- 📱 **Responsive web interface** with modern UI
- 🔐 **User authentication** and personalized watchlists
- 📊 **Portfolio performance** tracking
- 📰 **Market news** integration with sentiment analysis
- 📈 **Historical data** analysis with comprehensive OHLC data

## Tech Stack

### Frontend
- React with TypeScript
- Material-UI for modern UI components
- Chart.js for interactive visualizations
- Redux for state management
- Axios for API communication

### Backend
- FastAPI (Python)
- PostgreSQL database
- SQLAlchemy ORM
- JWT authentication
- Alpha Vantage API for stock data
- News API for market sentiment
- **yfinance** for reliable historical data
- **scikit-learn** for machine learning predictions
- **Technical Analysis (ta)** library for indicators

## Project Structure

```
stock-predictive-analytics/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── store/          # Redux store and slices
│   │   └── services/       # API services
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
├── ml_models/              # Machine learning models
└── docs/                   # Project documentation
```

## 🚀 Quick Start Options

### Option 1: Docker (Recommended - No Dependencies Required!)

**Prerequisites**: Install Docker and Docker Compose
- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/

```bash
# Clone the repository
git clone https://github.com/yourusername/Stock_Predictive_AnalyticsTracker.git
cd Stock_Predictive_AnalyticsTracker

# Start with Docker (everything included!)
./docker-start.sh

# Stop Docker containers
./docker-stop.sh
```

**That's it!** 🎉 The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Option 2: Local Development (One-Time Setup)

#### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Stock_Predictive_AnalyticsTracker.git
cd Stock_Predictive_AnalyticsTracker
```

#### 2. Run the setup script (ONCE ONLY)
```bash
./setup.sh
```

#### 3. Start the application
```bash
./start_all.sh
```

That's it! 🎉 The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

## 🛠️ Easy Startup Options

### Docker Commands
```bash
# Start everything with Docker
./docker-start.sh

# Stop Docker containers
./docker-stop.sh

# View logs
docker-compose logs -f

# Rebuild and start
docker-compose up --build -d
```

### Local Development Commands
```bash
# Start both servers (Recommended)
./start_all.sh

# Start individual servers
./start_backend.sh  # Backend only
./start_frontend.sh # Frontend only

# Manual startup
source venv/bin/activate
cd backend && PYTHONPATH=. python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
cd frontend && npm start
```

## 🐳 Docker Features

### Multi-Stage Builds
- **Backend**: Python 3.10 with optimized dependencies
- **Frontend**: Node.js 18 → Nginx production build
- **Database**: PostgreSQL 15 (optional)

### Production Ready
- **Health checks** for all services
- **Nginx reverse proxy** with API routing
- **Gzip compression** and security headers
- **Environment variable** configuration
- **Volume persistence** for database

### Easy Deployment
```bash
# Development
docker-compose up -d

# Production (with database)
docker-compose --profile database up -d

# Custom environment
ALPHA_VANTAGE_API_KEY=your_key docker-compose up -d
```

## 🔑 API Keys Required

For full functionality, you'll need:
- **Alpha Vantage API Key**: For real-time stock data
- **News API Key**: For market news and sentiment analysis

Get free API keys from:
- Alpha Vantage: https://www.alphavantage.co/support/#api-key
- News API: https://newsapi.org/register

**Note**: The app works in demo mode without API keys for testing!

## 📊 New API Endpoints

### Comprehensive Stock Data
```
GET /api/v1/stocks/comprehensive/{symbol}
```
Returns:
- Current price and change
- Previous day OHLC data
- Current day OHLC data
- Timestamp

### Stock Predictions
```
GET /api/v1/stocks/predictions/{symbol}?days=7
```
Returns:
- Daily price predictions
- Confidence scores
- Model accuracy

### Prediction Summary
```
GET /api/v1/stocks/prediction-summary/{symbol}
```
Returns:
- Average prediction
- Trend analysis (bullish/bearish)
- Confidence percentage
- Trend strength

## 🎯 Usage Examples

### Search for a Stock
1. Enter a stock symbol (e.g., AAPL, GOOGL, MSFT)
2. Click "Search" to fetch comprehensive data
3. View current price, previous day data, and predictions

### View Predictions
- Toggle prediction visibility with the eye icon
- See 7-day price forecasts with confidence scores
- Analyze trend direction and strength

### Technical Analysis
- View price movement charts
- Compare previous vs current day performance
- Monitor technical indicators

## 🤖 Machine Learning Features

The prediction system uses:
- **Random Forest Regressor** for price forecasting
- **Technical Indicators**: RSI, MACD, Bollinger Bands, Moving Averages
- **Feature Engineering**: Price changes, volatility, volume analysis
- **Model Evaluation**: Train/test split with accuracy scoring

## 🔧 Development

### Docker Development
```bash
# Start with hot reload
docker-compose up --build

# View logs
docker-compose logs -f backend

# Rebuild specific service
docker-compose build backend
```

### Local Development
```bash
# Backend
./start_backend.sh

# Frontend
./start_frontend.sh
```

### Testing
```bash
# Backend tests
cd backend
python3 -m pytest

# Frontend tests
cd frontend
npm test
```

## 📈 Data Sources

- **Real-time Data**: Alpha Vantage API
- **Historical Data**: yfinance library
- **Technical Indicators**: TA-Lib calculations
- **News & Sentiment**: News API
- **Predictions**: Custom ML models

## 🚀 Deployment Options

### Docker Deployment
```bash
# Local deployment
./docker-start.sh

# Production deployment
docker-compose --profile database up -d

# Custom environment
ALPHA_VANTAGE_API_KEY=your_key NEWS_API_KEY=your_key docker-compose up -d
```

### Cloud Deployment
```bash
# Heroku
heroku create your-app-name
git push heroku main

# AWS ECS
aws ecs create-service --cluster your-cluster --service-name stock-analytics

# Google Cloud Run
gcloud run deploy stock-analytics --source .
```

### Manual Deployment
```bash
# Backend
cd backend
pip install -r requirements.txt
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run build
npx serve -s build -l 3000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: This is a demo application. For production use, ensure proper API keys, security measures, and error handling are implemented. 