# Elobot
credits for major parts of the script: [Edgars2007](https://www.wikidata.org/wiki/User:Edgars2007) and [Tobias1984](https://www.wikidata.org/wiki/User:Tobias1984)


Python script written for importing [elo ratings](https://en.wikipedia.org/wiki/Elo_rating_system)
of chess players to [wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page). Source is [FIDE](http://ratings.fide.com/).

Script uses [pywikibot](https://github.com/wikimedia/pywikibot-core) library.

##TODO:
* script should check if the exact statement (rating value and date) does exist, if it does, it
should skip the item to prevent duplicate values
* files opened by the script should be closed
