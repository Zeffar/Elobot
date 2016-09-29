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

####################################################################writing to wd

for player in itemList:
	wdItem = player[0]
	fideId = player[1]
	
	if fideId not in fideRatings:
		pywikibot.output("Did not find fide id: " +fideId+" for WD item: " + wdItem)
		print("_______________________________________________\n")
		didntFind.write("{}\t{}\",\n".format(wdItem,fideId))
		continue
		
	rating = fideRatings[fideId]
	outputstring = "Item:{},FIDE ID:{},Rating:{}".format(wditem,fideid,rating)
	file.write(outputstring+'\n')
####################################################################writing claim

	print("Setting P1087 claim to "+wdItem+", value of "+ rating +".")
	playerItem = pywikibot.ItemPage(repository, wdItem)
	eloClaim = pywikibot.Claim(repository, u"P1087")
	eloClaim.setTarget(pywikibot.WbQuantity(rating))
	playerItem.addClaim(eloClaim)
	
####################################################################writing qualifier - date

	print("	Setting qualifier - date: april 2013.")#CHANGE THIS ON NEW RUN
	dateQualifier = pywikibot.Claim(repository, u"P585")
	date = pywikibot.WbTime(site=repository, year=2013, month=4)#CHANGE THIS ON NEW RUN
	dateQualifier.setTarget(date)
	eloClaim.addQualifier(dateQualifier)
	
####################################################################writing sources - stated in + date of retrieval and FIDE ID	

	print("		Setting source - stated in ratings.fide.com.")
	statedInProperty = pywikibot.Claim(repository, u"P248") 
	fideWeb = pywikibot.ItemPage(repository, u"Q27038151")
	statedInProperty.setTarget(fideWeb)
	print("		Setting source - retrieved on 21.9.2016.")
	retrievedProperty = pywikibot.Claim(repository, u"P813")
	dateQualifier = pywikibot.WbTime(site=repository, year=2016, month=9, day=21)
	retrievedProperty.setTarget(dateQualifier)
	print("		Setting source - fide id: " + fideId +".")
	fideIdProperty = pywikibot.Claim(repository, u"P1440") 
	fideIdProperty.setTarget(fideId)
	eloClaim.addSources([statedInProperty, retrievedProperty, fideIdProperty])
	print("Writing to "+wdItem+ " is done.")
	print("_______________________________________________\n")
	
print("All is done.")

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
