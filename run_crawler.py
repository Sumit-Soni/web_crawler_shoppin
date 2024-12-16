from tasks import crawl_website
import pandas as pd

# List of e-commerce domains
domains = [
    "http://example1.com/",
    "http://example2.com/",
    "http://example3.com/"
]

def submit_tasks():
  results = []
    for domain in domains:
        result = crawl_website.delay(domain)
        print(f"Task for {domain} submitted, Task ID: {result.id}")
        results.extend(result)
    data = pd.DataFrame(data={"urls": results})
    data.to_csv("urls.csv")
      

if __name__ == '__main__':
    submit_tasks()
