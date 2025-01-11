from db import SessionLocal
from scheduler import Scheduler
from product import Product

if __name__ == "__main__":
    # List of products to monitor
    products = [
        Product("stock", "AAPL", "Apple"),
        Product("stock", "MSFT", "Microsoft"),
        Product("stock", "GOOGL", "Google"),
    ]

    # Instantiate the scheduler
    scheduler = Scheduler(
        products=products,
        interval=3600,
        per_page=10,
        session_factory=SessionLocal,  # Run every hour
    )

    # Run the scheduler job
    scheduler.run_job()
