import csv

ld_names = ["LD", "VLD", "Varsity LD", "Lincoln Douglas", "Varsity Lincoln Douglas", "Lincoln-Douglas Debate", "Open LD", "Open Lincoln Douglas"]
pf_names = ["PF", "PFD", "VPF", "Varsity PF", "Public Forum", "Varsity Public Forum", "Public Forum Debate", "Open PF", "Open Public Forum"]
policy_names = ["CX", "VCX", "Varsity CX", "Policy", "Varsity Policy", "Policy Debate", "Open CX", "Open Policy", "Varisty Policy Debate", "Glendinning Varisty Policy"]

wiki_dict = {}
wiki_reader = csv.reader(open("wiki_data.csv", 'r'))
next(wiki_reader)
for row in wiki_reader:
    name = " ".join(row[1:3]).lower()
    wiki_dict[name] = row

def main():
    tournaments = ["harvard2019", "hw2019", "bronx2018", "cal2019"]
    for tourn in tournaments:
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
    print("At " + id + ", of "+str(total) + " entries, " + str(has_wiki) + " have a wiki while "+ str(rr) +" disclose round reports and " + str(os) + " disclose open source.")
    print("This means " + str(round(has_wiki/total* 100, 2)) + " percent have a wiki, and " + str(round(os/total * 100, 2)) + " percent open source.")


if __name__ == "__main__":
    main()