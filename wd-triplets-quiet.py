import json
import urllib.parse
import requests
import pywikibot

REPOSITORY = pywikibot.Site("wikidata", "wikidata").data_repository()
FILE = open("elo-item-rating-triplet.csv", "w", encoding="utf-8")
NOT_FOUND = open("item-fide-id-match-not-found.csv", "w", encoding="utf-8")
QUERY_STRING = """SELECT ?item ?value
WHERE
{
    ?item wdt:P1440 ?value .
}
"""
WD_QUERY = urllib.parse.quote(QUERY_STRING)
WD_QUERY_URL = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query={}&format=json".format(WD_QUERY)
URL = requests.get(WD_QUERY_URL)
JSON_DATA = json.loads(URL.text)
ITEM_LIST = [[data["item"]["value"].replace("http://www.wikidata.org/entity/", ""),\
    data["value"]["value"]] for data in JSON_DATA["results"]["bindings"]]
FIDE_RATING_FILE = open("pairs.csv", "r", encoding="utf-8").read()
FIDE_RATING_FILE = FIDE_RATING_FILE.split("\n")
FIDE_RATING_FILE2 = [f for f in FIDE_RATING_FILE if len(f) > 0]
FIDE_RATING_FILE3 = [f.split(",") for f in FIDE_RATING_FILE2]
FIDE_RATINGS = {f[0]:f[1] for f in FIDE_RATING_FILE3}

FILE.write("qid,P1087,qal585,S813,S854,S1440\n")

for player in ITEM_LIST:
    WD_ITEM = player[0]
    FIDE_ID = player[1]
    if FIDE_ID not in FIDE_RATINGS:
        NOT_FOUND.write("Item:{}, FIDE ID:{}\n".format(WD_ITEM, FIDE_ID))
        continue
    RATING = FIDE_RATINGS[FIDE_ID]
    FILE.write("{},{},+2018-06-01T00:00:00Z/10,+2018-07-28T00:00:00Z/11,\"\"\"\"https://ratings.fide.com/download.phtml\",\"\"\"\"{}\"\n".format(WD_ITEM, RATING, FIDE_ID))

# +2018-06-01T00:00:00Z/10 for June 2018 elo rating, more at https://www.wikidata.org/wiki/Help:QuickStatements
# +2018-07-28T00:00:00Z/11 for claiming that rating was retrieved on 28/7/2018
