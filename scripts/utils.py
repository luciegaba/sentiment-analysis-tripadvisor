import time
import re
from selenium import webdriver # import webdriver from selenium package
from bs4 import BeautifulSoup
import random
import undetected_chromedriver as uc


def parse_url(url: str) -> BeautifulSoup:
    """
    Opens browser and loads the given url.
    Returns a BeautifulSoup object representing the page's source code.
    """

    options = webdriver.ChromeOptions()
    driver = uc.Chrome( options=options)
    driver.get(url)
    time.sleep(random.randint(8,15))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    return soup


def get_digits(string_to_digit: str,float_option=True):
    """
    Given a string, returns the first set of consecutive digits found as an int.
    If no digits are found, returns None.
    """

    if string_to_digit:
        if float_option == True:
            try:
                digit = float("".join(re.findall(r'[+-]?\d*\.\d+|\d+', string_to_digit)))
            except:
                digit = 0.0
        try:
            digit = int("".join(re.findall(r'\d+', string_to_digit)))
        except:
            digit = 0
        return digit


def flatten(lst: list) -> list:
    """
    Given a list of lists, returns a list containing all the items of the original list.
    """
    return [item for sublist in lst for item in sublist]
