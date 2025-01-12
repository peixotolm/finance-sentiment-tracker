import time
from datetime import datetime, timedelta, timezone

from app.core.logging import logger
from app.services.sentiment import Sentiment
from app.services.stock import StockData


class Scheduler:
    def __init__(
        self, products, interval, per_page, session_factory, stock_interval="5min"
    ):
        """
        Initializes the Scheduler.
        :param products: List of product objects to analyze.
        :param interval: Time interval (in seconds) for the scheduler job to run.
        :param per_page: Number of news items per page for the API.
        :param stock_interval: Interval for intraday stock data (e.g., '5min').
        """
        self.products = products
        self.interval = interval
        self.per_page = per_page
        self.stock_interval = stock_interval
        self.sentiment_history = {}  # Stores the last sentiment count for each product
        self.session_factory = session_factory

    def run_job(self):
        """
        Executes the scheduled job to fetch and process sentiment and stock data.
        """
        while True:
            logger.info("Starting analysis job...")
            current_time = datetime.now(timezone.utc)
            from_date = (
                current_time - timedelta(hours=24)
            ).isoformat()  # Last 24 hours
            to_date = current_time.isoformat()

            for product in self.products:
                try:
                    # Process Sentiment Analysis
                    logger.info(f"Processing sentiment for product: {product.title}")
                    sentiment_analyzer = Sentiment(
                        product=product,
                        per_page=self.per_page,
                        from_date=from_date,
                        to_date=to_date,
                    )
                    sentiment_analyzer.fetch_sentiment()
                    new_sentiment = sentiment_analyzer.get_sentiment_summary()
                    self._process_sentiment_change(product, new_sentiment)
                    sentiment_analyzer.save_to_db()

                    # Fetch Stock Data
                    logger.info(f"Fetching stock data for product: {product.title}")
                    stock_fetcher = StockData(symbol=product.title)
                    stock_data = stock_fetcher.get_intraday_data(
                        interval=self.stock_interval
                    )
                    if stock_data:
                        self._save_stock_data_to_db(product, stock_data)

                except Exception as e:
                    logger.error(f"Error processing product {product.title}: {e}")

            logger.info("Analysis job completed.")
            logger.info(f"Next job will run in {self.interval} seconds.")
            time.sleep(self.interval)

    def _process_sentiment_change(self, product, new_sentiment):
        """
        Compares the new sentiment data with the last known sentiment,
        logs changes in the predominant sentiment, and saves the sentiment data.
        :param product: The product being analyzed.
        :param new_sentiment: Dictionary with the latest sentiment data.
        """
        old_sentiment = self.sentiment_history.get(product.title, None)

        def get_predominant_sentiment(sentiment_counts):
            return max(sentiment_counts, key=sentiment_counts.get)

        new_predominant = get_predominant_sentiment(new_sentiment)
        old_predominant = (
            get_predominant_sentiment(old_sentiment) if old_sentiment else None
        )

        if old_predominant and old_predominant != new_predominant:
            logger.info(f"Sentiment shift for {product.title} detected!")
            logger.info(
                f"Shift: {old_predominant.upper()} -> {new_predominant.upper()}"
            )

        if not old_sentiment:
            logger.info(f"Initial sentiment data recorded for {product.title}.")

        self.sentiment_history[product.title] = new_sentiment

    def _save_stock_data_to_db(self, product, stock_data):
        """
        Saves stock data to the database.
        :param product: Product being analyzed.
        :param stock_data: Intraday stock data.
        """
        try:
            with self.session_factory() as session:
                from db import StockData  # Import dynamically to avoid circular imports

                # Extract the latest data point
                time_series = stock_data.get("Time Series (5min)")
                if not time_series:
                    logger.warning(f"No stock data found for {product.title}")
                    return

                latest_timestamp = sorted(time_series.keys())[-1]
                latest_data = time_series[latest_timestamp]

                stock_record = StockData(
                    product_name=product.title,
                    date=datetime.fromisoformat(latest_timestamp),
                    price=float(latest_data["4. close"]),
                    volume=int(latest_data["5. volume"]),
                )
                session.add(stock_record)
                session.commit()

                logger.info(f"Stock data for {product.title} saved to the database.")

        except Exception as e:
            logger.error(f"Error saving stock data for {product.title}: {e}")
