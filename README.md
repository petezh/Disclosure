# Tab/Wiki Analysis

#### Introduction

I started the Tab/Wiki project May of 2020. The project analyzes disclosure data from 2014 to 2021, cross-referencing entry data from 295 tournaments. There are two portions to this project: scraping and analysis.

#### Scrapers

I built scrapers for [Tabroom](http://tabroom.com/) and the [wiki](https://hsld.debatecoaches.org/). They are located in the `Wiki Scraper.ipynb` and `Tab Scraper.ipynb` notebooks.

The wiki scraper gathers information on the disclosure practices and position names of every listed team. It visits every school and checks every team's aff and neg page. Then, it collects information on each listed round and the name of each cite, storing them in `wiki_data`.

The text of the cites were not collected because of encoding errors. This may be added in a future edition.

Each wiki page has a couple hundred schools and a few thousand teams. To scrape a new wiki page, add a new URL to the `tools/wiki_pages.csv` document. Then, specify the target pages in the settings of the `Wiki_Scraper.ipynb` notebook.

The Tabroom scraper collects the entries from each tournament. It iterates through the posted divisions and categorizes them according to the event name lists in the `tools` folder. It then collects all the available information from each page of entries and stores these in `wiki_data`.

The scraper also collects general information on the tournament, including location and dates. These are also stored in `wiki_data`.

To add a new tournament, add a new tournament ID and tournament name pair to the `ld_tourns.csv` file.

All data for the project are available in the `tab_data` and `wiki_data` folders. The wiki data are disaggregated by tournament. 

An important reminder for anyone who plans to use them: please **do not scrape** Tabroom or the Wiki during tournaments. If possible, restrict scraping to weekday nights. These sites are already overloaded during those times and scrapers exacerbate that problem.

#### Analysis

The analysis is conducted in `Disclosure Analysis.ipynb`. The write-up is found in the `Article.md` file.

#### Contact

This project was part of a larger collection of scraping and analysis tools related to debate. If you're interested in learning more, reach out to me on [Facebook](https://www.facebook.com/petejzh/) or at [petez@berkeley.edu](mailto:petez@berkeley.edu).
