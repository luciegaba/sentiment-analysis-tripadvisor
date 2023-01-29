import time
import os
import re
import pandas as pd
from selenium import webdriver # import webdriver from selenium package
from bs4 import BeautifulSoup
import random
import undetected_chromedriver as uc
from collections import Counter
import matplotlib.figure


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


def get_digits(string_to_digit: str):
    """
    Given a string, returns the first set of consecutive digits found as an int.
    If no digits are found, returns None.
    """
    try:
        digit = float("".join(re.findall(r'[+-]?\d*\.\d+|\d+', string_to_digit)))
    except:
        digit = 0.0
    return digit


def flatten(lst: list) -> list:
    """
    Given a list of lists, returns a list containing all the items of the original list.
    """
    return [item for sublist in lst for item in sublist]




def counter(var: list) -> dict:
    """
    Compute and return a dictionary of the frequency count of each unique element in a given list.
    The returned dictionary is sorted in descending order based on the frequency count.

    Parameters:
        - var (list): The input list whose elements will be counted.

    Returns:
        dict: A dictionary with the frequency count of each unique element in the input list.
    """
    var_counter = Counter(var)
    var_counter = dict(sorted(var_counter.items(), key=lambda x: x[1], reverse=True))
    return var_counter



def get_data(path:str) -> pd.DataFrame:
    """ Import data for app """
    data=pd.read_json(path+"/data/clean_data.json")
    return data

def save_plots_png(figure:matplotlib.figure.Figure, name_fig:str, filepath:str="", repo:str="") -> None:
    """
    This function saves a given figure as a .png file in a specified directory.
    If the file already exists, it will be overwritten.
    
    Parameters:
        figure : The figure to be saved.
        name_fig : The name of the saved file.
        filepath : The filepath where the figure will be saved. If None, the filepath will be created using the repo and the name_fig.
        repo : The repository where the figure will be saved. If None, it will be extracted from the name_fig.
    """
    if not filepath:
        if not repo:
            repo = name_fig.split("_")[0]
        filepath = os.path.dirname(os.path.dirname(os.getcwd())) + f"/{repo}/" + name_fig
    if os.path.isfile(filepath):
        os.remove(filepath)  
    figure.savefig(filepath+name_fig,transparent=True)