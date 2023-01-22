import time
import re
from selenium import webdriver # import webdriver from selenium package
from random import randint
from bs4 import BeautifulSoup

def get_driver_options() -> webdriver.ChromeOptions:
    """
    Returns a ChromeOptions object with various configurations set.
    These configurations are intended to prevent the browser from being detected as a web scraper.
    """
    configs = [
        "--disable-extensions",
        "--disable-dev-shm-usage",
        "--no-sandbox",
        "--headless",
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "--incognito"
    ]
    options = webdriver.ChromeOptions()
    for argument in configs:
        options.add_argument(argument)
    return options


def parse_url(url: str) -> BeautifulSoup:
    """
    Opens a headless browser and loads the given url.
    Returns a BeautifulSoup object representing the page's source code.
    """
    driver = webdriver.Chrome(options= get_driver_options())
    driver.get(url)
    soup = None
    while soup is None:
        try:
            time.sleep(randint(5, 7))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.close()
        except:
            print("An error occured, retrying in 5 seconds")
            time.sleep(5)
    return soup


def get_digits(string_to_digit: str) -> int:
    """
    Given a string, returns the first set of consecutive digits found as an int.
    If no digits are found, returns None.
    """
    if string_to_digit:
        try:
            digit = int("".join(re.findall(r'\d+', string_to_digit)))
        except:
            digit = None
        return digit


def flatten(lst: list) -> list:
    """
    Given a list of lists, returns a list containing all the items of the original list.
    """
    return [item for sublist in lst for item in sublist]
