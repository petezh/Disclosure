"""
Clean
Does compiling and cleaning for datasets
@author petez
"""

import csv

# to analyze
TOURNAMENTS = ["harvard19", "yale18", "grapevine18", "greenhill18", "cal19", "hwestlake19", "blake18", "scarsdale18", "goldendesert19"]

# get LD, PF, and CX event names
LD_NAMES = [name for name in open('tools/ld_eventnames.txt', 'r')]
PF_NAMES = [name for name in open('tools/pf_eventnames.txt', 'r')]
CX_NAMES = [name for name in open('tools/cx_eventnames.txt', 'r')]

wiki_dict = {}
wiki_reader = csv.reader(open("wiki_data.csv", 'r'))

next(wiki_reader)

for row in wiki_reader:
    name = " ".join(row[1:3]).lower()
    wiki_dict[name] = row

def main():
    
    for tourn in TOURNAMENTS:
        checkTournament(tourn)

def checkTournament(id):
    
    tab_data = csv.reader(open("tab_data/" + id + ".csv", 'r'))
    header = next(tab_data)

    total = 0
    has_wiki = 0
    rr = 0
    os = 0
    for row in tab_data:
        event_index = header.index("Event")
        if row[event_index] in ld_names:
            total += 1
            entry_index = header.index("Entry")
            name = row[entry_index].lower()
            
            if name in wiki_dict:
                has_wiki += 1
                
                practices = wiki_dict[name]
                if int(practices[6]) > 0:
                    rr += 1
                if int(practices[7]) > 0:
                    os += 1
    print("Tournament " + id + " Entries: "+str(total))
    print("Percent Wiki: " + str(round(has_wiki/total* 100, 2)) + " Percent RReports: " + str(round(rr/total * 100, 2)) + " Percent OSource: " + str(round(os/total * 100, 2)))


if __name__ == "__main__":
    main()