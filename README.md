# Stock and Sentiment Tracker

This project is designed to analyze the sentiment of financial news and track stock performance for specific companies. It fetches real-time stock data using the Alpha Vantage API and processes news sentiment using the Apitube API. The data is stored in a local SQLite database for further analysis.

---

## Features

- **Sentiment Analysis**: Analyze financial news articles and classify them as positive, neutral, or negative.
- **Stock Data Tracking**: Retrieve intraday stock prices, including open, close, high, low, and volume.
- **Database Storage**: Save stock and sentiment data for historical reference and trend analysis.
- **Scheduler**: Automatically run jobs at regular intervals to keep data updated.

---

## Prerequisites

- Python 3.8 or later
- SQLite (installed locally or use built-in Python support)
- API keys for:
  - [Alpha Vantage API](https://www.alphavantage.co/)
  - [Apitube API](https://apitube.io/)

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-repo-url/stock-sentiment-tracker.git
cd stock-sentiment-tracker
```
2. Create a virtual environment:

```bash
poetry shell
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables: Create a .env file in the project root with the following contents:

```plaintext
DATABASE_URL=sqlite:///local_database.db
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
APITUBE_API_KEY=your_apitube_api_key
```

5. Initialize the database:

```bash
python main.py
```

## Project Structure

```plaintext
.
├── db.py                 # Database models and configuration
├── scheduler.py          # Scheduler for running periodic jobs
├── sentiment.py          # Sentiment analysis logic
├── stock_data_fetcher.py # Stock data fetcher class
├── main.py               # Entry point for the application
├── logging_config.py     # Logging configuration
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not included in repo)
├── README.md             # Project documentation
```

## APIs Used

1. Alpha Vantage API

Provides real-time and historical stock market data.

API Documentation
[Alpha Vantage API](https://www.alphavantage.co/)

2. Apitube API - Used for news sentiment analysis.

API Documentation
[Apitube API](https://apitube.io/)

Known Issues
API Limits: Ensure you don't exceed the free tier limits of the APIs.
Database Growth: Regularly archive or clean up the database if it grows too large.

## Contribution

1. Fork the repository.

2. Create a feature branch:

```bash
git checkout -b feature/your-feature
```

3. Commit your changes:

```bash
git commit -m "Add your feature description"
```

4. Push to the branch:
```bash
git push origin feature/your-feature
```

5. Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For any questions or issues, please create an issue in the repository or contact the project maintainer.
