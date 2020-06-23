import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import csv

def main():

    url = "https://www.cnn.com/2020/06/21/opinions/trump-roasted-for-tulsa-rally-crowd-size-obeidallah/index.html"
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    text = soup.find_all('div', {'class' : 'zn-body__paragraph'})
    paragraphs = [paragraph.text for paragraph in text]
    article = "\n".join(paragraphs)
    print(article)
    


if __name__ == "__main__":
    main()
