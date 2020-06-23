import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import csv

aberdeen_url = "https://hsld18.debatecoaches.org/Aberdeen%20Central/"
ab_url= "https://hsld18.debatecoaches.org/Acton-Boxborough/"
def main():

    url = "https://hsld18.debatecoaches.org/"
    schools = getSchools(url)

    school_writer = csv.writer(open("schools_wiki.csv", 'w'), lineterminator = "\n")
    school_writer.writerow(["School Name", "Entries"])

    for school in schools:
        school_name = school[0]
        school_url = "https://hsld18.debatecoaches.org/" + school[1]

        print(school_name + " is...")
        table = checkSchool(school_url)
        if not isinstance(table, str):
            school_writer.writerow([school_name, len(table)])

            for index, row in table.iterrows():
                print(row['Debater'])

        else:
            school_writer.writerow([school_name, 0])
            print(0)
            

# for a given archive year, return all schools
def getSchools(url):

    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all('a')
    school_links = [link for link in links if "(" in link.text and ")" in link.text]
    schools = [[link.text, link.get('href')] for link in school_links]

    return schools

def checkSchool(url):

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
        return "No disclosure!"

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

    return datatable




if __name__ == "__main__":
    main()
