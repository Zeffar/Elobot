# Elobot
A python script written for importing [elo ratings](https://en.wikipedia.org/wiki/Elo_rating_system) mined from [FIDE ratings](http://ratings.fide.com/) to the [wikidata database](https://www.wikidata.org/wiki/Wikidata:Main_Page).

Script uses [pywikibot](https://github.com/wikimedia/pywikibot-core) library.

It outputs batch prepared for [QuickStatements](https://tools.wmflabs.org/quickstatements/).

## Todo
* test with QuickStatements
* combine steps in Prepdata/script.txt and wd-triplets.py into one shellscript
* the dates are now hardcoded inside wd-triplets.py, ideally the script would be given a date (ex. 5/2018) and it would reuse it throughout the whole code
