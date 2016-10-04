# Elobot
Python script written for importing [elo ratings](https://en.wikipedia.org/wiki/Elo_rating_system) of chess players to [wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page).

Source of input data is [FIDE](http://ratings.fide.com/).

Credits for major parts of the script go to [Edgars2007](https://www.wikidata.org/wiki/User:Edgars2007), [Tobias1984](https://www.wikidata.org/wiki/User:Tobias1984) and [Matěj Suchánek](https://www.wikidata.org/wiki/User:Matěj_Suchánek).

Script uses [pywikibot](https://github.com/wikimedia/pywikibot-core) library.

##TODO high priority:
* script should check if the exact statement (rating value and date) does exist, if it does, it should skip the item to prevent duplicate values

##TODO low priority:
* rewrite the querying part and csv parsing part
* use input() for input files so they are not hardcoded into the script
* figure a way to "pause/resume" the script
