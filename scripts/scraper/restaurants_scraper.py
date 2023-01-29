import re
from scripts.utils import parse_url


def get_max_page_number(soup):
    """
    Returns the maximum page number from the given soup object.

    Parameters:
    - soup: bs4.BeautifulSoup object

    Returns:
    - int: maximum page number
    """
    results = int(soup.find("span", class_="SgeRJ").findChildren("span", "b")[0].text)
    return results


def get_pages_urls(url, max_page):
    """
    Returns the list of URLs for all the pages.

    Parameters:
    - url: str, URL of the first page
    - max_page: int, maximum page number

    Returns:
    - list of str, list of URLs for all the pages
    """
    urls = [url]
    codice = re.search("-g\d+-", url).group(0)
    link = url.replace(codice, codice + "oa30-")
    urls.append(link)
    for x in range(60, max_page, 30):
        new_link = re.sub(r"-oa\d+-", "-oa" + str(x) + "-", link)
        urls.append(new_link)
    return urls


def scrap_caracteristics(url):
    """
    Scrapes and returns the characteristics of a TripAdvisor page.

    Parameters:
    - url: str, URL of the TripAdvisor page

    Returns:
    - list of dictionaries, list of scraped characteristics,
      where each dictionary contains:
        - 'name': str, name of the attraction
        - 'url': str, URL of the attraction
        - 'nb_reviews': str, number of reviews
        - 'caracteristics': str, '?'-separated list of caracteristics
    """
    soup = parse_url(url)
    data = []
    try:
        nb_reviews = [type.text for type in soup.find_all("span", class_="IiChw")]
        names = [name.text for name in soup.find_all("a", class_="Lwqic Cj b")]
        urls = [
            "https://www.tripadvisor.fr" + url["href"]
            for url in soup.find_all("a", class_="Lwqic Cj b", href=True)
        ]
        nb_reviews = [type.text for type in soup.find_all("span", class_="IiChw")]
        caracteristics = [type.text for type in soup.find_all("span", class_="ABgbd")]
        sequences = split_on_avis(caracteristics)
        for name, url, nb_rev, seq in zip(names, urls, nb_reviews, sequences):
            data.append(
                {
                    "name": name,
                    "url": url,
                    "nb_reviews": nb_rev,
                    "caracteristics": "?".join(seq),
                }
            )
        return data
    except:
        pass


def split_on_avis(data):
    """
    Split a list of elements into sequences separated by the word "avis".

    Parameters:
    data (list): A list of elements to be split into sequences.

    Returns:
    list: A list of sequences, where each sequence is a list of elements from the original list.

    Example:
    split_on_avis(["A", "B", "avis", "C", "D", "E", "avis", "F", "G"])
    [['A', 'B', 'avis'], ['C', 'D', 'E', 'avis'], ['F', 'G']]
    """
    sequences = []
    temp = []
    for element in data:
        if "avis" in element:
            if temp:
                sequences.append(temp)
                temp = []
            temp.append(element)
        else:
            temp.append(element)
    sequences.append(temp)
    return sequences
