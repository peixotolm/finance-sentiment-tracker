from scheduler import Scheduler
from product import Product

if __name__ == "__main__":

    # List of products to monitor
    products = [Product("stock", "AAPL", "Apple"), Product("stock", "MSFT", "Microsoft"),
                Product("stock", "GOOGL", "Google")]

    # Instantiate the scheduler
    scheduler = Scheduler(
        products=products,
        interval=3600,  # Run every hour
        per_page=10
    )

    # Run the scheduler job
    scheduler.run_job()
