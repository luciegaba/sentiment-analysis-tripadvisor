
import urllib.request
import requests
import re
from utils import parse_url

def scrap_comments(main_url):
    reviews_customers_pages=[]
    reviews_customers_pages.append(main_url)
    reviews_scraped=[]
    nb_reviews=50
    for x in range(10,nb_reviews, 10):
        url=re.sub(r"Reviews-",f"Reviews-or{x}-",main_url)
        reviews_customers_pages.append(url)
    
    for page in reviews_customers_pages:
        response = requests.get(page,headers= { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
        status = response.status_code
        print(status)
        if status == 200:
            soup=parse_url(page)
            reviews= [title.text+": "+review.text for title,review in zip(soup.find_all("span",class_="noQuotes"),soup.find_all("p","partial_entry"))]
            reviews_scraped.append(reviews)
            print(page)
    return reviews_scraped