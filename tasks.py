import requests
from bs4 import BeautifulSoup
from celery import Celery
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

app = Celery('product_crawler', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

def extract_product_urls(page_content, base_url):
    soup = BeautifulSoup(page_content, 'html.parser')
    product_urls = []

    for link in soup.find_all('a', href=True):
        href = link['href']
        
        if re.search(r'/product/|/item/|/p/', href):
            if not href.startswith('http'):
                href = base_url + href
            product_urls.append(href)

    return product_urls

def crawl_with_requests(domain):
    product_urls = []
    try:
        response = requests.get(domain)
        if response.status_code == 200:
            product_urls = extract_product_urls(response.text, domain)
        else:
            print(f"Failed to fetch {domain}: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error crawling {domain}: {str(e)}")
    return product_urls

def crawl_with_selenium(domain):
    product_urls = []
    try:
        # Set up Selenium WebDriver (headless mode)
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(domain)
        
        time.sleep(3)  
      # to handle scrolling
        last_height = driver.execute_script("return document.body.scrollHeight")
    
        while True:
          driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
          time.sleep(2)
          new_height = driver.execute_script("return document.body.scrollHeight")
        
          if new_height == last_height:
              break
          last_height = new_height
        
        page_content = driver.page_source
        driver.quit()
        
        product_urls = extract_product_urls(page_content, domain)
    except Exception as e:
        print(f"Error using Selenium to crawl {domain}: {str(e)}")
    return product_urls

@app.task(bind=True, retry=True)
def crawl_website(self, domain):
    print(f"Crawling {domain}")
    
    product_urls = crawl_with_requests(domain)

    if not product_urls:
        print(f"Retrying {domain} with Selenium...")
        product_urls = crawl_with_selenium(domain)

    return product_urls
