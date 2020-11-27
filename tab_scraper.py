"""
Tabroom Scraper
Gets tournament info and entry information from the ID number of tournaments.
@author petez & ehu
"""

# imports
import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import csv
import os.path
from os import path

# controls
OVERWRITE = False

# point to CSV with tournaments
TOURNAMENT_CSV = 'tourn_data/tourn_info.csv'

# get LD, PF, and CX event names
LD_NAMES = [name for name in open('tools/ld_eventnames.txt', 'r')]
PF_NAMES = [name for name in open('tools/pf_eventnames.txt', 'r')]
CX_NAMES = [name for name in open('tools/cx_eventnames.txt', 'r')]

# set events to scrape
TARGET_EVENTS = ["LD", "PF", "CX"]

def main():

    # read tourn list
    with open(TOURNAMENT_CSV, 'r') as tourn_file:

        tourn_reader = csv.reader(tourn_file)

        # skip headers
        headers = next(tourn_reader)

        # create new list
        tourn_rows = [headers]
        
        # for all selected tourns
        for tourn in tourn_reader:
                
            # get tourn name and url
            tourn_name = tourn[0]
            tourn_id = tourn[1]

            print("Checking", tourn_name)

            # if info is incomplete, get info
            if len(tourn) < 6:
                tourn_rows += [[tourn_name, tourn[1]] + getInfo(tourn_id)]
            else:
                tourn_rows += [tourn]

            # check if entry data exists
            if(not NO_REPEAT & path.exists("tab_data/" + tourn_name + ".csv")):
                print("Exists already.\n")

            else:
                
                # frames for aggrevating results
                frames = []

                # go through events
                eventUrls = getEvents(tourn_id)

                for event_url in event_urls:
                    
                    # get info
                    event_rawName = event_url[0]
                    event_name = processName(event_rawName)
                    url = event_url[1]
                    
                    # append results
                    if event_name in TARGET_EVENTS:

                        # do scraping
                        print("Scraping", event)
                        frames = frames + [getEntries(url, event)]

                # send to csv
                if len(frames) == 0:
                    print("No entries found for ", tourn_name, "\n")

                else:
                    pd.concat(frames).to_csv("tab_data/" + tourn_name + ".csv")
                    print("Entries saved!\n")

    # write tourn info
    tourn_info = csv.writer(open(TOURNAMENT_CSV, 'w'), lineterminator = "\n")
    tourn_info.writerows(tourn_rows)

"""
getInfo gets tournamnet information from an invite page.
"""
def getInfo(tourn_id):

    url = "https://www.tabroom.com/index/tourn/index.mhtml?tourn_id=" + tourn_id

    # load page
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    # find header
    header = soup.select('h5')[0].text.strip()
    
    # get sub-header
    year = header.split('—')[0].strip()
    location = header.split('—')[1].strip()
    if ',' in location:
        city = location.split(',')[0].strip()
        state = location.split(',')[1].strip()
    
    else:
        city = "None"
        state = location

    # get info box
    info = soup.find_all('span', {'class' : 'smaller half'})[0].text
    date = ' '.join(info.split())

    return [date, year, city, state]

# from entries page, retrieves tagged urls for each event
def getEvents(tourn_id):
    
    url = "https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=" + tourn_id

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

"""
Helper functions
"""


# convert invite url to entries url
def toEntries(url):
    
    return url.replace("index.mhtml", "fields.mhtml")

def processName(raw_name):

    if raw_name in LD_NAMES:
        return "LD"

    if raw_name in PF_NAMES:
        return "PF"

    if raw_name in CX_NAMES:
        return "CX"

    return "None"

if __name__ == "__main__":
    main()
