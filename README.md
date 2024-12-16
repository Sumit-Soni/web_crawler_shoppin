# web crawler shoppin
A web crawler whose primary task is to discover and list all product URLs across multiple e-commerce websites.
Tech stack used - 
  - Python
  - Celery
  - Redis
Library used -
  - requests
  - BeautifulSoup
  - selenium

Steps to run :-
1. pip install -r requirements.txt
2. celery -A tasks worker --loglevel=info --concurrency=4
3. python run_crawler.py 
