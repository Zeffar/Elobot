import pywikibot, re, json, urllib.parse, requests

repository = pywikibot.Site("wikidata", "wikidata").data_repository()
output_file = open("chess-elo-item-rating-output.txt","w", encoding="utf-8")
didnt_find = open("chess-didntfind-fideid-output.txt","w", encoding="utf-8")
# items_from_source_not_written = open("items_from_csv_source_not_written.txt","w", encoding="utf-8")

####################################################################querying wd, output in json

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
# item_list_for_output = item_list

####################################################################get input from csv

fide_rating_file = open("standard_apr14.csv", "r", encoding="utf-8").read()#CHANGE THIS ON NEW RUN
fide_rating_file = fide_rating_file.split("\n")
fide_rating_file2 = [f for f in fide_rating_file if len(f)>0]
fide_rating_file3 = [f.split(",") for f in fide_rating_file2]
fide_ratings = {f[0]:f[1] for f in fide_rating_file3}

####################################################################writing to wd
counter = 1
for player in item_list:
	try:
		wd_item = player[0]
		fide_id = player[1]
		
		if fide_id not in fide_ratings:
			print("Did not find fide id: " + str(fide_id) + " for WD item: " + str(wd_item))
			print("_______________________________________________\n")
			didnt_find.write("Item:{},FIDE ID:{}\n".format(wd_item,fide_id))
			continue
			
		rating = fide_ratings[fide_id]
		output_file.write("Item:{},FIDE ID:{},Rating:{}\n".format(wd_item,fide_id,rating))
####################################################################writing claim
		print("Writing statement number: " + str(counter))
		print("Setting P1087 claim to " + str(wd_item) + ", value of " + str(rating) + ".")
		player_item = pywikibot.ItemPage(repository, wd_item)
		elo_claim = pywikibot.Claim(repository, u"P1087")
		elo_claim.setTarget(pywikibot.WbQuantity(rating))
		player_item.addClaim(elo_claim)
		counter = counter + 1
		
####################################################################writing qualifier - date

		print("	Setting qualifier - date: April 2014.")#CHANGE THIS ON NEW RUN
		date_qualifier = pywikibot.Claim(repository, u"P585")
		date = pywikibot.WbTime(site=repository, year=2014, month=4)#CHANGE THIS ON NEW RUN
		date_qualifier.setTarget(date)
		elo_claim.addQualifier(date_qualifier)
		
####################################################################writing sources - stated in + date of retrieval and FIDE ID	

		print("		Setting source - stated in ratings.fide.com.")
		stated_in_property = pywikibot.Claim(repository, u"P248") 
		fideWeb = pywikibot.ItemPage(repository, u"Q27038151")
		stated_in_property.setTarget(fideWeb)
		print("		Setting source - retrieved on 21.9.2016.")
		retrieved_on_property = pywikibot.Claim(repository, u"P813")
		date_qualifier = pywikibot.WbTime(site=repository, year=2016, month=9, day=21)
		retrieved_on_property.setTarget(date_qualifier)
		print("		Setting source - fide id: " + str(fide_id) +".")
		fide_id_property = pywikibot.Claim(repository, u"P1440") 
		fide_id_property.setTarget(fide_id)
		elo_claim.addSources([stated_in_property, retrieved_on_property, fide_id_property])
		print("Writing to " + str(wd_item) + " is done.")
		print("_______________________________________________\n")
		# item_list_for_output.pop(player)
	except pywikibot.NoPage:
		print(str(wd_item) + "does not exist. Skipping")
		player.next()
		continue

output_file.close()
didnt_find.close()
# items_from_source_not_written.write(item_list_for_output)
# items_from_source_not_written.close()
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
