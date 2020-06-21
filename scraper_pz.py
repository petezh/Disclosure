import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


def main():
    url = input("Enter url: ")
    getMenu(toEntries(url))

# convert invite url to entries url
def toEntries(url):
    return url.replace("index.mhtml", "fields.mhtml")


# take an entries page and visit each url
def getMenu(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    urls = [link.get('href') for link in soup.find_all('a')]
    event_urls = [url for url in urls if "event_id" in url]

    for url in event_urls:
        print(getTable("https://www.tabroom.com" + url))

# extract table from a page

def getTable(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find_all("table")[0]
    n_rows = 0
    n_columns = 0
    column_names = []

    for row in table.find_all('tr'):
        td = row.find_all('td')
        if len(td) > 0:
            n_rows = n_rows + 1
            if n_columns == 0:
                n_columns = len(td)

        th = row.find_all('th')
        if len(th) > 0 and len(column_names) ==0:
            for header in th:
                column_names.append(header.get_text().strip())
    if len(column_names) > 0 and len(column_names) != n_columns:
        raise Exception("Column titles do not match the number of columns")

    columns = column_names if len(column_names) > 0 else range(0, n_columns)
    datatable = pd.DataFrame(columns = columns, index = range(0, n_rows))
    row_marker = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            datatable.iat[row_marker, column_marker] = column.get_text().strip()
            column_marker = column_marker + 1
        if len(columns) > 0:
            row_marker = row_marker +1
    return datatable.to_string()

if __name__ == "__main__":
    main()
