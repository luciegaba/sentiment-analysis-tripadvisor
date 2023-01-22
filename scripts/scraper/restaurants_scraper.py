
import re
from scripts.utils import parse_url

def get_max_page_number(soup):
    results=int(soup.find("span",class_="SgeRJ").findChildren("span","b")[0].text)
    return results

def get_pages_urls(url,max_page):
    urls = [url]
    codice = re.search("-g\d+-", url).group(0)
    link = url.replace(codice, codice + "oa30-")
    urls.append(link)
    for x in range(60, max_page, 30):
        new_link = re.sub(r"-oa\d+-", "-oa" + str(x) + "-", link)
        urls.append(new_link)
    return urls

def scrap_caracteristics(url):
    soup=parse_url(url)
    data=[]
    try:
        nb_reviews=[type.text for type in soup.find_all("span",class_="IiChw")]
        names=[name.text for name in soup.find_all("a",class_="Lwqic Cj b")]
        urls=["https://www.tripadvisor.fr"+url["href"] for url in soup.find_all("a",class_="Lwqic Cj b",href=True)]
        nb_reviews=[type.text for type in soup.find_all("span",class_="IiChw")]
        caracteristics=[type.text for type in soup.find_all("span",class_="ABgbd")]    
        sequences=split_on_avis(caracteristics)
        for name,url,nb_rev,seq in zip(names,urls,nb_reviews,sequences):
            data.append({"name":name,"url":url,"nb_reviews":nb_rev,"caracteristics":"?".join(seq)})
        return data
    except:
        pass
    
def split_on_avis(data):
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





    






