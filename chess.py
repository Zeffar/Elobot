import pywikibot, re, json, urllib.parse, requests, time
####################################################################open external files
fide_rating_file = open("standard_apr14.csv", "r", encoding="utf-8").read() #CHANGE ACCORDINGLY
found_output_file = open("chess-elo-item-rating-output.txt","w", encoding="utf-8")
didnt_find_output_file = open("chess-didntfind-fideid-output.txt","w", encoding="utf-8")
####################################################################set variables for writing to wd
year_of_rating = 2014 #CHANGE ACCORDINGLY
month_of_rating = 4 #CHANGE ACCORDINGLY
year_of_retrieval = 2016 #CHANGE ACCORDINGLY
month_of_retrieval = 9 #CHANGE ACCORDINGLY
day_of_retrieval = 21 #CHANGE ACCORDINGLY
repository = pywikibot.Site("wikidata", "wikidata").data_repository()
stated_in_property = u"P248"
stated_in_claim = pywikibot.Claim(repository, stated_in_property)
retrieved_on_property = u"P813"
retrieved_on_claim = pywikibot.Claim(repository, retrieved_on_property)
fide_web_item = u"Q27038151"
fide_web_item_page = pywikibot.ItemPage(repository, fide_web_item)
elo_property = u"P1087"
elo_claim = pywikibot.Claim(repository, elo_property)
fide_id_property = u"P1440"
fide_id_claim = pywikibot.Claim(repository, fide_id_property) 
date_property = u"P585"
date_claim = pywikibot.WbTime(year = year_of_rating, month = month_of_rating)
date_qualifier = pywikibot.WbTime(year = year_of_retrieval, month = month_of_retrieval, day = day_of_retrieval)
horizontal_line = "_______________________________________________\n"
####################################################################query wd, output in json
query_string = """SELECT ?item ?value
WHERE
{
?item wdt:P1440 ?value .
}
"""
wd_query = urllib.parse.quote(query_string)
wd_query_url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query={}&format=json".format(wd_query)
url = requests.get(wd_query_url)
json_data = json.loads(url.text)
item_list = [[data["item"]["value"].replace("http://www.wikidata.org/entity/",""),data["value"]["value"]] for data in json_data["results"]["bindings"]]
####################################################################parse csv input
fide_rating_file = fide_rating_file.split("\n")
fide_rating_file2 = [f for f in fide_rating_file if len(f)>0]
fide_rating_file3 = [f.split(",") for f in fide_rating_file2]
fide_ratings = {f[0]:f[1] for f in fide_rating_file3}
####################################################################write to wd
counter = 1
for player in item_list:	
	try:
		wd_item = player[0]
		fide_id = player[1]
		if fide_id not in fide_ratings:
			print(("Did not find fide id: {} for WD item: {}.\n{}").format(fide_id, wd_item, horizontal_line))
			didnt_find_output_file.write(("Item:{},FIDE ID:{}\n").format(wd_item,fide_id))
			continue
		rating = fide_ratings[fide_id]
####################################################################write claims
		print(("Writing statement number: {}").format(counter))
		print(("Setting P1087 claim to {}, value of {}.").format(wd_item,rating))
		player_item = pywikibot.ItemPage(repository, wd_item)
		elo_claim.setTarget(pywikibot.WbQuantity(rating))
		player_item.addClaim(elo_claim)
####################################################################write qualifier - date
		print(("	Setting qualifier - date property: year: {}, month: {}.").format(year_of_rating, month_of_rating))
		date_qualifier.setTarget(date_claim)
		elo_claim.addQualifier(date_qualifier)
####################################################################write sources - stated in + date_property of retrieval and FIDE ID	
		print("		Setting source - stated in {}.".format(fide_web_item))
		stated_in_claim.setTarget(fide_web_item_page)
		print(("		Setting source - retrieved on {}, month: {}.").format(year_of_retrieval, month_of_retrieval))
		retrieved_on_claim.setTarget(retrieved_on_property)
		print(("		Setting source - fide id: {}.").format(fide_id_property))
		fide_id_claim.setTarget(fide_id_property)
		elo_claim.addSources([stated_in_claim, retrieved_on_claim, fide_id_claim])
		print(("Writing to {} is done.\n{}".format(wd_item, horizontal_line))
		found_output_file.write(("Item: {},FIDE ID: {},Rating: {}.\n").format(wd_item,fide_id,rating))
		counter = counter + 1
		time.sleep(60)
	except pywikibot.NoPage:
		print(("{} does not exist. Skipping.\n{}").format(wd_item, horizontal_line))
		player.next()
		continue
####################################################################End
found_output_file.close()
didnt_find_output_file.close()
print(("Wrote {} claims.").format(counter))
####################################################################Cheatsheet
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
# property P585 "date_property" to be found at https://www.wikidata.org/wiki/Property:P585
# property P1087 "elo" to be found at https://www.wikidata.org/wiki/Property:1087
# property P1440 "fide id", to be found at https://www.wikidata.org/wiki/Property:P1440
# item "ratings.fide.com" to be found at https://www.wikidata.org/wiki/Q27038151
