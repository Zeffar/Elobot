import pywikibot, re, json, urllib.parse, requests

repository = pywikibot.Site("wikidata", "wikidata").data_repository()
file = open("chess-elo-item-rating-output.txt","w", encoding="utf-8")
didntFind = open("chess-didntfind-fideid-output.txt","w", encoding="utf-8")

####################################################################querying wd, output in json

queryString = """SELECT ?item ?value
WHERE
{
	?item wdt:P1440 ?value .
}
"""

wdQuery = urllib.parse.quote(queryString)
wdQueryUrl = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query={}&format=json".format(wdQuery)
url = requests.get(wdQueryUrl)
json_data = json.loads(url.text)
itemList = [[data["item"]["value"].replace("http://www.wikidata.org/entity/",""),data["value"]["value"]] for data in json_data["results"]["bindings"]]

####################################################################get input from csv

fideRatingFile = open("standard_apr13.csv", "r", encoding="utf-8").read()#CHANGE THIS ON NEW RUN
fideRatingFile = fideRatingFile.split("\n")
fideRatingFile2 = [f for f in fideRatingFile if len(f)>0]
fideRatingFile3 = [f.split(",") for f in fideRatingFile2]
fideRatings = {f[0]:f[1] for f in fideRatingFile3}

print("This script writes the matches between wikidata player items and fide ids to external files - chess-elo-item-rating-output.txt and chess-didntfind-fideid-output.txt. It does not write to wikidata.")

for player in itemList:
	wdItem = player[0]
	fideId = player[1]
	
	if fideId not in fideRatings:
		didntFind.write("Item:{},FIDE ID:{}\n".format(wdItem,fideId))
		continue
		
	rating = fideRatings[fideId]
	file.write("Item:{},FIDE ID:{},Rating:{}\n".format(wdItem,fideId,rating))
	
print("Done.")

####################################################################
# jan		1
# feb		2
# mar		3
# apr		4
# may		5
# jun		6
# jul		7
# aug		8
# sep		9
# oct		10
# nov		11
# dec		12
# property P813 "retrieved", to be found at https://www.wikidata.org/wiki/Property:P813
# property P248 "stated in", to be found at https://www.wikidata.org/wiki/Property:P248
# property P585 "date" to be found at https://www.wikidata.org/wiki/Property:P585
# property P1087 "elo" to be found at https://www.wikidata.org/wiki/Property:1087
# property P1440 "fide id", to be found at https://www.wikidata.org/wiki/Property:P1440
# item "ratings.fide.com" to be found at https://www.wikidata.org/wiki/Q27038151
