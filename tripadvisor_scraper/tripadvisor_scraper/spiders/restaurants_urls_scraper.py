import scrapy
import os
from dotenv import load_dotenv
load_dotenv()

from tripadvisor_scraper.items import RestaurantItem

class TripAdvisorSpider(scrapy.Spider):
    name = "restaurants_urls_scraper"  # Define the name for scraper (used in command line to launch spider)
    def __init__(self, start_url="https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html#EATERY_LIST_CONTENTS", *args, **kwargs):
        super().__init__(*args, **kwargs)     #Pass argument start url (initial page to scrap) 
        self.start_urls = [start_url]   


    custom_settings = {
        "FEEDS": {
            "sentiment-analysis-tripadvisor/data/restaurants_urls.csv": {"format": "csv"} #Define export file and options like overwrite 
        }
    }

    def parse(self, response):
        """Main method for parsing the response page"""
        for restaurant_selector in response.css("span > div.zqsLh div.zdCeB"):     # For restaurant 1,2,3 ... in page n
            restaurant = self.parse_restaurant(restaurant_selector)                # We get elements from parse_restaurant method
            yield restaurant

        next_page = response.css("a.nav.next::attr(href)").get()                   #Action that get url available in "next" button corresponding to the following page
        if next_page is not None:                                                  #Until the page is not None (it will end the crawl process if None)
            yield response.follow(next_page, self.parse)

    def parse_restaurant(self, restaurant_selector):
        """Method for parsing the information of a restaurant"""
        name = restaurant_selector.css("div.RfBGI span a::text")[-1].get()         
        url = "https://www.tripadvisor.fr" + restaurant_selector.css("div.RfBGI span a::attr(href)").get()    
        return RestaurantItem(name=name, url=url)                                  #  RestaurantItem defined in items.py
 