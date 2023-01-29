import re
from scripts.utils import parse_url


def scrap_comments(main_url):
    """
    Given a restaurant review, this function collect a chosen number of reviews from customers by parsing pages and get fields with BeautifulSoup
    :param main_url: string, review_url
    :param timeout: int, the maximum time (in seconds) to wait for the geocoding service
    :return: a tuple of floats (latitude, longitude)
    """
    reviews_customers_pages = []
    reviews_customers_pages.append(main_url)
    reviews_scraped = []
    nb_reviews = 50
    for x in range(10, nb_reviews, 10):
        url = re.sub(r"Reviews-", f"Reviews-or{x}-", main_url)
        reviews_customers_pages.append(url)

    for page in reviews_customers_pages:
        soup = parse_url(page)
        reviews = [
            title.text + ": " + review.text
            for title, review in zip(
                soup.find_all("span", class_="noQuotes"),
                soup.find_all("p", "partial_entry"),
            )
        ]
        reviews_scraped.append(reviews)
        print(page)
    return reviews_scraped
