import time
import logging
from datetime import datetime, timedelta, timezone
from sentiment import Sentiment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self, products, interval, per_page):
        """
        Initializes the Scheduler.
        :param products: List of product objects to analyze.
        :param interval: Time interval (in seconds) for the scheduler job to run.
        :param per_page: Number of news items per page for the API.
        """
        self.products = products
        self.interval = interval
        self.per_page = per_page
        self.sentiment_history = {}  # Stores the last sentiment count for each product

    def run_job(self):
        """
        Executes the scheduled job to fetch and process sentiment data.
        """
        while True:
            logger.info("Starting sentiment analysis job...")
            current_time = datetime.now(timezone.utc)
            # Define the time range for the analysis
            from_date = (
                current_time - timedelta(hours=24)
            ).isoformat()  # Last 24 hours
            to_date = current_time.isoformat()

            for product in self.products:
                logger.info(f"Processing sentiment for product: {product.title}")

                # Create a Sentiment instance for the current product
                sentiment_analyzer = Sentiment(
                    product=product,
                    per_page=self.per_page,
                    from_date=from_date,
                    to_date=to_date,
                )

                # Fetch sentiment and compare with previous state
                sentiment_analyzer.fetch_sentiment()
                self._process_sentiment_change(
                    product, sentiment_analyzer.get_sentiment_summary()
                )

            logger.info("Sentiment analysis job completed.")
            logger.info(f"Next job will run in {self.interval} seconds.")

            # Wait for the specified interval before the next job
            time.sleep(self.interval)

    def _process_sentiment_change(self, product, new_sentiment):
        """
        Compares the new sentiment data with the last known sentiment,
        logs changes in the predominant sentiment, and saves the sentiment data.
        :param product: The product being analyzed.
        :param new_sentiment: Dictionary with the latest sentiment data.
        """
        old_sentiment = self.sentiment_history.get(product.title, None)

        # Determine predominant sentiment
        def get_predominant_sentiment(sentiment_counts):
            return max(sentiment_counts, key=sentiment_counts.get)

        new_predominant = get_predominant_sentiment(new_sentiment)
        old_predominant = (
            get_predominant_sentiment(old_sentiment) if old_sentiment else None
        )

        # Log predominant sentiment change
        if old_predominant and old_predominant != new_predominant:
            logger.info(f"Sentiment shift for {product.title} detected!")
            logger.info(
                f"Shift: {old_predominant.upper()} -> {new_predominant.upper()}"
            )

        # Log initial recording if no prior sentiment
        if not old_sentiment:
            logger.info(f"Initial sentiment data recorded for {product.title}.")

        # Save new sentiment to the database
        sentiment_analyzer = Sentiment(
            product=product,
            per_page=self.per_page,
            from_date=datetime.now(timezone.utc).isoformat(),  # Current timestamp
            to_date=datetime.now(timezone.utc).isoformat(),
        )
        sentiment_analyzer.sentiment_count = (
            new_sentiment  # Populate the sentiment count
        )
        sentiment_analyzer.save_to_db()

        # Update sentiment history
        self.sentiment_history[product.title] = new_sentiment
