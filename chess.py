import requests, pywikibot, re, json, urllib.parse

repo = pywikibot.Site("wikidata", "wikidata").data_repository()
file = open("chess-out.txt","w", encoding="utf-8")
didntfound = open("chess-out-didntfound.txt","w", encoding="utf-8")

####################################################################json

QUERY = """SELECT ?item ?value
WHERE
{
	?item wdt:P1440 ?value .
}
"""

query2 = urllib.parse.quote(QUERY)

url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query={}&format=json".format(query2)
url2= requests.get(url)

json_data = json.loads(url2.text)

itemlist = [[data["item"]["value"].replace("http://www.wikidata.org/entity/",""),data["value"]["value"]] for data in json_data["results"]["bindings"]]


####################################################################tsv
fideratingfile = open("standard_mar16frl_xml.csv", "r", encoding="utf-8").read()

fideratingfile = fideratingfile.split("\n")

fideratingfile2 = [f for f in fideratingfile if len(f)>0]
fideratingfile3 = [f.split("\t") for f in fideratingfile2]
fideratings = {f[0]:f[1] for f in fideratingfile3}

####################################################################tsv

for player in itemlist:
	wditem = player[0]
	fideid = player[1]
	
	if fideid not in fideratings:
		pywikibot.output("did not found id: " +fideid+" from WD item: " + wditem)
		didntfound.write("{}\t{}\",\n".format(wditem,fideid))
		continue
		
	rating = fideratings[fideid]
	outputstring = "\"{}\":\"{}\",".format(wditem,rating)
	print("Setting P1087 claim to "+wditem+", value of "+rating)
	playerItem = pywikibot.ItemPage(repo, wditem)
	eloClaim = pywikibot.Claim(repo, u"P1087") # property "elo" to be found at https://www.wikidata.org/wiki/Property:1087
	eloClaim.setTarget(pywikibot.WbQuantity(rating))
	playerItem.addClaim(eloClaim)
	qualifier = pywikibot.Claim(repo, u"P585") # property "date" to be found at https://www.wikidata.org/wiki/Property:P585
	date = pywikibot.WbTime(site=repo, year=2016, month=3)
	print("Setting qualifier: date 3.2016")
	qualifier.setTarget(date)
	eloClaim.addQualifier(qualifier)
	statedin = pywikibot.Claim(repo, u"P248") # property "URL (reference)" to be found at https://www.wikidata.org/wiki/Property:P854
	fideweb = pywikibot.ItemPage(repo, u"Q27038151") # item "ratings.fide.com" to be found at https://www.wikidata.org/wiki/Q27038151
	statedin.setTarget(fideweb)
	print("Setting qualifier: stated in ratings.fide.com")
	retrieved = pywikibot.Claim(repo, u"P813") # property "retrieved" to be found at https://www.wikidata.org/wiki/Property:P813
	dateofretrieval = pywikibot.WbTime(site=repo, year=2016, month=9, day=21)
	print("Setting qualifier: retrieved on 21.9.2016")
	retrieved.setTarget(dateofretrieval)
	eloClaim.addSources([statedin, retrieved])
print("Done")