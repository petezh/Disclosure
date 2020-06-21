import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import csv

# event names
ld_names = ["LD", "VLD", "Varsity LD", "Lincoln Douglas", "Varsity Lincoln Douglas", "Lincoln-Douglas Debate", "Open LD", "Open Lincoln Douglas"]
pf_names = ["PF", "PFD", "VPF", "Varsity PF", "Public Forum", "Varsity Public Forum", "Public Forum Debate", "Open PF", "Open Public Forum"]
policy_names = ["CX", "VCX", "Varsity CX", "Policy", "Varsity Policy", "Policy Debate", "Open CX", "Open Policy"]

# set events to scrape
events = ld_names + pf_names + policy_names

def main():

    # get tournament list
    tournies = csv.reader(open("tournaments.csv", 'r'))

    # skip headers
    next(tournies)
    
    # for all selected tournies
    for tourny in tournies:

        tourny_name = tourny[0]
        url = "https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=" + tourny[1]
        print("Trying " + tourny_name)

        # get events
        event_urls = getEvents(url)

        frames = []
        
        for event_url in event_urls:
            
            url = event_url[1]
            event = event_url[0]
            
            # append results
            if event in events:
                print(event)
                frames = frames + [getEntries(url, event)]

        # send to csv
        if len(frames) == 0:
            print("No entries found for " + tourny_name)
        else:
            pd.concat(frames).to_csv(tourny_name + ".csv")
            

# convert invite url to entries url
def toEntries(url):
    
    return url.replace("index.mhtml", "fields.mhtml")


# from entries page, retrieves tagged urls for each event
def getEvents(url):
    
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    
    return [[link.contents[0].strip(), "https://www.tabroom.com" + link.get('href')] for link in soup.find_all('a') if "event_id" in link.get('href')]

# extract table from a page
def getEntries(url, event):
    
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

    datatable["Event"] = event
    
    return datatable

if __name__ == "__main__":
    main()
