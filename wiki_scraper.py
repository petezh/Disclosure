"""
Wiki Scraper
Collects information off the NDCA High School wikis.
@author petez
"""


import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import csv

PAGES = [["LD18", "https://hsld18.debatecoaches.org/"], ["LD17", "https://hsld17.debatecoaches.org/"]]


def main():
    
    for page in PAGES:
        
        page_name = page[0]
        page_url = page[1]

        schools = getSchools(page_url)

        school_writer = csv.writer(open("wiki_data/" + page_name + "schools_wiki.csv", 'w'), lineterminator = "\n")
        school_writer.writerow(["School Name", "Entries"])

        debater_writer = csv.writer(open("wiki_data/" + page_name + "debaters_wiki.csv", 'w'), lineterminator = "\n")
        debater_writer.writerow(["State", "School", "First", "Last", "Side", "Rounds", "Cites", "Round Reports", "Open Source", "Full Text", "Facebook?"])

        num_schools = len(schools)
        counter = 0

        for school in schools:

            counter += 1

            school_code = school[0]
            school_name = " ".join(school_code.split()[:-1])

            state = school_code.split()[-1].strip('()')
            school_url = url + school[1]

            print(school_name, str(counter),"/", str(num_schools))
            table = checkSchool(school_url)
            if not isinstance(table, str):
                school_writer.writerow([school_name, len(table)])

                for index, row in table.iterrows():
                    debater_name = row['Debater']
                    first_name = debater_name.split()[-2]
                    last_name = debater_name.split()[-1]
                    aff_results = checkPage(school_url + "/" + last_name + "%20Aff")
                    neg_results = checkPage(school_url + "/" + last_name + "%20Neg")
                    debater_writer.writerow([state, school_name, first_name, last_name, "Aff"] + aff_results)
                    debater_writer.writerow([state, school_name, first_name, last_name, "Neg"] + neg_results)

            else:
                school_writer.writerow([school_name, 0])
            

# for a given archive year, return all schools
def getSchools(url):

    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all('a')
    school_links = [link for link in links if "(" in link.text and ")" in link.text]
    schools = [[link.text, link.get('href')] for link in school_links]

    return schools

def checkSchool(url):

    try:
        html = urlopen(url).read()
    except Exception:
        return "Broken!"
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

cite_writer = csv.writer(open("wiki_data/debaters_cites.csv", 'w'), lineterminator = "\n")

   

def checkPage(url):

    
    try:
        html = urlopen(url).read()
    except Exception:
        return [-1, -1, -1, -1]
    
    soup = BeautifulSoup(html, "html.parser")
    
    tables = len(soup.find_all("table"))

    # round reports
    if tables > 0:
        table = soup.find_all("table")[0]
    else:
        return [-1, -1, -1, -1]
    
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
        total_rounds = 0
    else:
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
        
        total_rounds = len(datatable)

    # cites box
    

    total_rr = str(html).count("report.png")
    total_os = len(soup.find_all(text=lambda x: x and ".docx" in x))
    
    facebook = False
    full_text = 0
    cites = soup.find_all("div", {"name": "entry"})
    total_cites = len(cites)

    for cite in cites:
        text = cite.text
        
        if "facebook" in text:
            facebook = True
        if len(text) > 8000:
            full_text += 1
        cite_writer.writerow([len(text)])

    return [total_rounds, total_cites, total_rr, total_os, full_text, facebook]
    

if __name__ == "__main__":
    main()
