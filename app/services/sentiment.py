import requests
from decouple import config

from app.core.database import SessionLocal
from app.core.logging_conf import logger
from app.models.sentiment import SentimentData

APITUBE_API_KEY = config("APITUBE_API_KEY")


class Sentiment:
    def __init__(self, product, per_page, from_date, to_date):
        self.product = product
        self.sentiment_count = {"positive": 0, "neutral": 0, "negative": 0}
        self.per_page = per_page
        self.from_date = from_date
        self.to_date = to_date

    def fetch_sentiment(self):
        """
        Fetch sentiment data from the API and update sentiment counters.
        """

        URL = "https://api.apitube.io/v1/news/everything"

        querystring = {
            "from": self.from_date,
            "to": self.to_date,
            "category": "finance",
            "title": self.product.title,
            "language": "en",
            "api_key": APITUBE_API_KEY,
            "per_page": self.per_page,
        }

        try:
            # Make the API request
            response = requests.get(URL, params=querystring)
            response.raise_for_status()  # Raise exception for HTTP error codes
            results = response.json().get("results", [])

            if not results:
                logger.warning(f"No results found for product: {self.product.title}")
                return

            # Process the results
            self._process_results(results)
            logger.info(
                f"Sentiment analysis completed for product: {self.product.title}"
            )

        except requests.exceptions.RequestException as e:
            logger.error(
                f"API request failed for product: {self.product.title}. Error: {e}"
            )

    def _process_results(self, results):
        """
        Process API results to update sentiment counters.
        :param results: List of results returned by the API.
        """
        for result in results:
            try:
                sentiment = result["sentiment"]["overall"]["polarity"]
                if sentiment in self.sentiment_count:
                    self.sentiment_count[sentiment] += 1
                else:
                    logger.warning(f"Unexpected sentiment type: {sentiment}")
            except KeyError as e:
                logger.warning(
                    f"Missing expected key in result for product: \
                    {self.product.title}. Error: {e}"
                )

    def get_sentiment_summary(self):
        """
        Returns a summary of the collected sentiment data.
        :return: Dictionary containing sentiment counters.
        """
        return self.sentiment_count

    def save_to_db(self):
        """
        Save the sentiment counts to the database.
        """
        session = SessionLocal()
        try:
            sentiment_entry = SentimentData(
                product_name=self.product.title,
                positive_count=self.sentiment_count["positive"],
                neutral_count=self.sentiment_count["neutral"],
                negative_count=self.sentiment_count["negative"],
            )
            session.add(sentiment_entry)
            session.commit()
            logger.info(f"Sentiment data saved for {self.product.title}.")
        except Exception as e:
            logger.error(f"Failed to save sentiment data for {self.product.title}: {e}")
            session.rollback()
        finally:
            session.close()
