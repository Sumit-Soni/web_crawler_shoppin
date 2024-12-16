from celery import Celery

# Set up Celery app
app = Celery('product_crawler', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

app.conf.update(
    task_routes = {'tasks.crawl_website': {'queue': 'crawl_queue'}},
    task_retry_limit = 5,
    task_default_retry_delay = 60  # Retry after 60 seconds in case of failure
)
