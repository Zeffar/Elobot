# Elobot
A python script written for importing [elo ratings](https://en.wikipedia.org/wiki/Elo_rating_system) mined from [FIDE ratings](http://ratings.fide.com/) to the [wikidata database](https://www.wikidata.org/wiki/Wikidata:Main_Page).

Script uses [pywikibot](https://github.com/wikimedia/pywikibot-core) library.

It outputs batch prepared for [QuickStatements](https://tools.wmflabs.org/quickstatements/).

## Dependencies
* xmlstarlet
* python3
* python module requests
* wget
* unzip
* paste

## Todo
* test with QuickStatements
* wd-triplets.py could generate date of elo and date retrieved according to argument of elofetch.sh
