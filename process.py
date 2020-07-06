# Extracts results URLs from Raul's TOC Calendar (thank you Raul!)
# @author petez

import pandas as pd
import csv

def main():
    convertLD()

def convertLD():
    
    # get list of tournaments
    insheet = csv.reader(open('cleaned.csv', 'r'))
    headers = next(insheet)

    outsheet = csv.writer(open('processed.csv', 'w'), lineterminator='\n')
    outsheet.writerow(["Name", "URL"])

    for row in insheet:
        name = row[0]
        id17 = row[5]
        id18 = row[6]

        adder = 1
        if row[7] == 'y':
            adder = 0

        if id17 != "Error":
            outsheet.writerow([name + str(17+adder), id17])
        
        if id18 != "Error":
            outsheet.writerow([name + str(18+adder), id18])


# excluded bluekey, sunvite, myerspark

def cleanLD():

    # read excel file
    exceldata = pd.read_excel("calendar.xlsx",sheet_name = "Sheet1")

    # find columns
    col_results17 = exceldata['LD 17-18 Results']
    col_results18 = exceldata['LD 18-19 Results']
    col_fullName = exceldata['LD Tournament']
    col_shortHand = exceldata['LD Shorthand']

    # outfile
    outsheet = csv.writer(open('cleaned.csv','w'),lineterminator = '\n')
    outsheet.writerow(["code", "fullname", "shorthand", "results17", "results18", "id17", "id18"])

    # iterate rows
    for i in exceldata.index:

        results17 = col_results17[i]
        results18 = col_results18[i]
        fullName = col_fullName[i]
        shortHand = col_shortHand[i]

        if "tourn_id=" in str(results17):
            end = results17.split("tourn_id=")[1]
            if "&" in end:
                id17 = end.split("&")[0]
            else:
                id17 = end
        else:
            id17 = "Error"

        if "tourn_id=" in str(results18):
            end = results18.split("tourn_id=")[1]
            if "&" in end:
                id18 = end.split("&")[0]
            else:
                id18 = end
        else:
            id18 = "Error"

        outsheet.writerow(["", fullName, shortHand, results17, results18, id17, id18])

if __name__ == "__main__":
    main()
