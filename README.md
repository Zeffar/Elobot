# Elobot
A python script written for importing [elo ratings](https://en.wikipedia.org/wiki/Elo_rating_system) mined from [FIDE ratings](http://ratings.fide.com/) to the [wikidata database](https://www.wikidata.org/wiki/Wikidata:Main_Page).

Credits for major parts of the script go to [Edgars2007](https://www.wikidata.org/wiki/User:Edgars2007) and [Matěj Suchánek](https://www.wikidata.org/wiki/User:Matěj_Suchánek).

Script uses [pywikibot](https://github.com/wikimedia/pywikibot-core) library.

## TODO:
* rewrite the querying part -  see "wd_sparql_generator" function at [Edoredoo's script](https://www.wikidata.org/wiki/User:Edoderoobot/en-nl-label-fixer)
* rewrite the csv parsing part - it should take as input original xml instead of csv - ongoing work at snippet [parse_xml.py](https://github.com/Wesalius/snippets/blob/master/parse_xml.py)
* split elobot function into smaller functions