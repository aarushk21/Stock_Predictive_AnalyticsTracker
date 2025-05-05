# Stock Predictive Analytics Tracker

A professional-grade stock market analysis and prediction platform that combines real-time market data, technical analysis, and machine learning to provide comprehensive stock insights and predictions.

## Features

- 📈 Real-time stock data tracking and visualization
- 🤖 Machine learning-based price predictions
- 📊 Technical analysis indicators and patterns
- 📱 Responsive web interface
- 🔐 User authentication and personalized watchlists
- 📊 Portfolio performance tracking
- 📰 Market news integration with sentiment analysis
- 📈 Historical data analysis

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

## Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/yourusername/Stock_Predictive_AnalyticsTracker.git
cd Stock_Predictive_AnalyticsTracker
```

2. Set up the backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend
```bash
cd frontend
npm install
```

4. Configure environment variables
- Create `.env` files in both frontend and backend directories
- Add necessary API keys and configuration

5. Run the application
```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm start
```

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for the complete API documentation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - [Your Email]
Project Link: [https://github.com/yourusername/Stock_Predictive_AnalyticsTracker](https://github.com/yourusername/Stock_Predictive_AnalyticsTracker) 