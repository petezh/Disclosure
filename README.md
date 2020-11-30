# Tab/Wiki Research

The Tab/Wiki Research project was started in May of 2020. There are two portions to this project: scraping and analysis.

**Note**: Please do not scrape Tabroom or the Wiki during tournament dates (weekends). If possible, restrict scraping to weekday nights.

## Scraping

There are two sets of scrapers.

### Wiki Scraping

The wiki scraper gets information on the disclosure practices and position names of every listed team. It visits every school and checks every team's aff and neg page. Then, it collects information on each listed round and the name of each cite.

> The text of the cites were not collected because of encoding errors. To study the text of the positions, use the open source links and download word documents.

Each wiki page has 300-500 schools and 2000-3000 teams. To scrape a new wiki page, add a new URL to the `wiki_pages.csv` document. 

### Tab Scraping

The tab scraper collects several sources of information.

#### Tournaments

list of tournament and tournament names

- nat cir bid tournaments

#### Paradigms

seahces thorugh all public paradigms, a-z, collects every link

> To scrape the 







