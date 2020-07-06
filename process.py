# Extracts results URLs from Raul's TOC Calendar (thank you Raul!)
# @author petez

import pandas as pd
import csv

def main():

    # read excel file
    exceldata = pd.read_excel("calendar.xlsx",sheet_name = "Sheet1")

    # find columns
    col_results17 = exceldata['LD 17-18 Results']
    col_results18 = exceldata['LD 18-19 Results']
    col_fullName = exceldata['LD Tournament']
    col_shortHand = exceldata['LD Shorthand']

    # outfile
    outsheet = csv.writer(open('cleaned.csv','w'),lineterminator = '\n')

    # iterate rows
    for i in exceldata.index:

        results17 = col_results17[i]
        results18 = col_results18[i]
        fullName = col_fullName[i]
        shortHand = col_shortHand[i]

        if "tourn_id=" in str(results17):
            idNum = results17.split("tourn_id=")[1]
        else:
            idNum = "Error"

        outsheet.writerow([results17, results18, fullName, shortHand, idNum])

if __name__ == "__main__":
    main()
