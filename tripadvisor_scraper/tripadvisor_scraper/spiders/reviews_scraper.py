import pandas as pd
from six.moves.urllib.parse import urljoin

from tripadvisor_scraper.items import ReviewtItem
import scrapy
import random
import requests

# class ReviewSpider(scrapy.Spider):
#     name = "reviews"
#     reviews = []
#     custom_settings = {
#         'FEEDS': { 'data/fetch_data.json': { 'format': 'json'}}
#         }


#     def start_requests(self):
#         fetch_urls=pd.read_csv("data/restaurants_urls.csv")
#         urls_to_parse=fetch_urls["url"].values.tolist()
#         selected_urls=random.sample(urls_to_parse,1000) # We randomly select 1000 elements for our analysis
#         #selected_urls=urls_to_parse
#         for listing in selected_urls:
#                 url = urljoin('http://www.tripadvisor.com', listing)
#                 yield scrapy.Request(url=url, callback=self.parse)
                
        
#     def parse(self, response):

#         name = response.css("h1.HjBfq ::text").get()
#         url=response.url
#         avg = response.css("span.ZDEqb::text").get()
#         price_and_cuisines = response.css("a.dlMOJ::text").getall()
#         nb_reviews=response.css("span.AfQtZ::text").get()
#         ranking=response.css("div.cNFlb b span::text").get()
#         location=response.css("span.yEWoV::text").get()
#         quartier=response.css("span.yEWoV OkcwQ::text").get()
#         reviews=[title+":"+body for title,body in zip(response.css("span.noQuotes::text").getall(),response.css("p.partial_entry::text").getall())]
#         yield {
#                         'url': url,
#                         'name': name,
#                         'average note': avg,
#                         'tripadvisor rank': ranking,
#                         'price and cuisines': price_and_cuisines,
#                         'number reviews': nb_reviews,
#                         'location':location,
#                         'quartier':quartier,
#                         'reviews':reviews,
#                     } 







class ReviewSpider(scrapy.Spider):
    name = "reviews_scraper"
    custom_settings = {'FEEDS': {'data/fetch_data.json': {'format': 'json', 'overwrite':'True'}}}

    def __init__(self, sample_size=1000, *args, **kwargs): #Create an argument for sample size which can be passed in argument of crawler like scrapy crawl reviews -a sample_size=2000
        super().__init__(*args, **kwargs)
        self.sample_size = sample_size


    def start_requests(self):
        fetch_urls = pd.read_csv("data/restaurants_urls.csv")
        urls_to_parse = fetch_urls["url"].values.tolist()
        if self.sample_size > len(urls_to_parse) or self.sample_size < 1:
            raise ValueError("Sample size must be between 1 and the number of URLs to parse")
        else:

            selected_urls = random.sample(urls_to_parse, self.sample_size) #
            for listing in selected_urls:
                url = urljoin('http://www.tripadvisor.com', listing)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """Parse restaurant page"""
        item = ReviewtItem() 
        item['url'] = response.url
        item['name'] = self._get_name(response)
        item['average_note'] = self._get_average_note(response)
        item['price_and_cuisines'] = self._get_price_and_cuisines(response)
        item['number_reviews'] = self._get_number_reviews(response)
        item['ranking'] = self._get_ranking(response)
        item['location'] = self._get_location(response)
        item['reviews'] = self._get_reviews(response)
        yield item

    def _get_name(self, response):
        """Extract the name of the restaurant from the response"""
        return response.css("h1.HjBfq ::text").get()

    def _get_average_note(self, response):
        """Extract the average note of the restaurant from the response"""
        return response.css("span.ZDEqb::text").get()

    def _get_price_and_cuisines(self, response):
        """Extract the price and cuisines of the restaurant from the response"""
        return response.css("a.dlMOJ::text").getall()

    def _get_number_reviews(self, response):
        """Extract the number of reviews of the restaurant from the response"""
        return response.css("span.AfQtZ::text").get()

    def _get_ranking(self, response):
        """Extract the ranking of the restaurant from the response"""
        return response.css("div.cNFlb b span::text").get()

    def _get_location(self, response):
        """Extract the location of the restaurant from the response"""
        return response.css("span.yEWoV::text").get()

    def _get_reviews(self, response):
        """Extract the 10 first reviews of the restaurant from the response"""
        return [title+":"+body for title,body in zip(response.css("span.noQuotes::text").getall(),response.css("p.partial_entry::text").getall())]


