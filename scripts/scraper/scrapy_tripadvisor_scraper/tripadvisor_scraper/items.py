# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RestaurantItem(scrapy.Item):
    """
    Defines the structure of the data that represents a restaurant. It has two fields:
    -  name field is used to store the name of the restaurant
    - url field is used to store the URL of the restaurant's page on the website.

    """

    name = scrapy.Field()
    url = scrapy.Field()


class ReviewtItem(scrapy.Item):
    """
    Defines the structure of the data that represents a review of a restaurant. It has several fields:

    - url: the url of the restaurant
    - name: the name of the restaurant
    - average_note: the average note of the restaurant
    - tripadvisor_rank: the rank of the restaurant on tripadvisor
    - price_and_cuisines: the price and cuisines of the restaurant
    - number_reviews: the number of reviews on the restaurant
    - location: the location of the restaurant
    - quartier: the neighborhood of the restaurant
    - reviews: the reviews of the restaurant
    """

    url = scrapy.Field()
    name = scrapy.Field()
    average_note = scrapy.Field()
    ranking = scrapy.Field()
    price_and_cuisines = scrapy.Field()
    number_reviews = scrapy.Field()
    location = scrapy.Field()
    quartier = scrapy.Field()
    reviews = scrapy.Field()
    traveller_choice = scrapy.Field()