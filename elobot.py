import pywikibot, re, json, urllib.parse, requests, time, winsound
# intro, assign variables
start_time = time.time()
repository = pywikibot.Site("wikidata", "wikidata").data_repository()
print("EloBot is a script for writing elo rating claims to wikidata - a collaboratively edited knowledge base operated by the Wikimedia Foundation.\n")
time.sleep(5)
input_csv_file = input("Give the name of the input csv file: ") # for example "standard_apr14.csv"
print("The following values must match the input csv file given above!\n")
time.sleep(5)
year_of_rating = int(input("Give the year of the rating: ")) # for ex "2014"
month_of_rating = int(input("Give the month of the rating: ")) # for ex "4" for April
year_of_retrieval = 2016 # year_of_retrieval = int(input("Give the year of the retrieval, for ex \"2016\": "))
month_of_retrieval = 9 # month_of_retrieval = int(input("Give the month of the retrieval, for ex \"9\" for September: "))
day_of_retrieval = 21 # day_of_retrieval = int(input("Give the day of the retrieval, for ex \"21\": "))
date_property = u"P585"
date_value = pywikibot.WbTime(year = year_of_rating, month = month_of_rating)
date_claim = pywikibot.Claim(repository, date_property)
stated_in_property = u"P248"
stated_in_claim = pywikibot.Claim(repository, stated_in_property)
retrieved_on_property = u"P813"
retrieved_on_value = pywikibot.WbTime(year = year_of_retrieval, month = month_of_retrieval, day = day_of_retrieval)
retrieved_on_claim = pywikibot.Claim(repository, retrieved_on_property)
fide_web_item = u"Q27038151"
fide_web_item_page = pywikibot.ItemPage(repository, fide_web_item)
elo_property = u"P1087"
elo_claim = pywikibot.Claim(repository, elo_property)
fide_id_property = u"P1440"
fide_id_claim = pywikibot.Claim(repository, fide_id_property) 
# open external files
with open(input_csv_file, "r", encoding="utf-8") as fide_csv_rating_file:
	with open("chess-elo-item-rating-output.txt", "w", encoding = "utf-8") as  found_output_file, open("chess-didntfind-fideid-output.txt", "w", encoding = "utf-8") as didnt_find_output_file:
# query wd, output in json
		print("\nProcessing {}, going to check and possibly write claims with the date qualifier - year {}, month {}, and sourced as retrieved on - year {}, month {}, day {}.\n".format(input_csv_file, year_of_rating, month_of_rating, year_of_retrieval, month_of_retrieval, day_of_retrieval))
		print("10 seconds until start.\n")
		time.sleep(10)
		query_string = """SELECT ?item ?value WHERE {?item wdt:P1440 ?value .}"""
		wd_query = urllib.parse.quote(query_string)
		wd_query_url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query={}&format=json".format(wd_query)
		url = requests.get(wd_query_url)
		json_data = json.loads(url.text)
		item_list = [[data["item"]["value"].replace("http://www.wikidata.org/entity/", ""), data["value"]["value"]] for data in json_data["results"]["bindings"]]
# parse csv input
		fide_rating_file = fide_csv_rating_file.read()
		fide_rating_file = fide_rating_file.split("\n")
		fide_rating_file2 = [f for f in fide_rating_file if len(f)>0]
		fide_rating_file3 = [f.split(",") for f in fide_rating_file2]
		fide_ratings = {f[0]:f[1] for f in fide_rating_file3}
# write to wd
		claim_counter = 1
		for player in item_list:
			has_claim_with_this_date = False
			wd_item = player[0]
			fide_id = player[1]
			player_item = pywikibot.ItemPage(repository, wd_item)
			player_item.get()
			for claim in player_item.claims.get(elo_property, []):
				for qualifier in claim.qualifiers.get(date_property, []):
					if qualifier.target_equals(date_value):
							has_claim_with_this_date = True
							print("Checking elo claim of the item {}. This elo claim has a qualifier stating date - year {}, month {}.\n".format(wd_item, year_of_rating, month_of_rating))
							break
			if has_claim_with_this_date:
				print("Checking elo claim of the item {}. This elo claim does not have a qualifier stating date - year {}, month {}.\n".format(wd_item, year_of_rating, month_of_rating))
				continue
			try:
				if fide_id not in fide_ratings:
					print(("Did not find fide id {} for item {}.\n").format(fide_id, wd_item))
					didnt_find_output_file.write(("Item:{}, FIDE ID:{}\n").format(wd_item,fide_id))
					continue
				rating = int(fide_ratings[fide_id])
# write claims
				print("Writing statement number: {}".format(claim_counter))
				print("Setting P1087 claim to {}, value of {}.".format(wd_item,rating))
				elo_claim.setTarget(pywikibot.WbQuantity(rating))
				player_item.addClaim(elo_claim)
# write qualifier - date
				print("	Setting qualifier - date: year {}, month {}.".format(year_of_rating, month_of_rating))
				date_claim.setTarget(date_value)
				elo_claim.addQualifier(date_claim)
# write sources - stated in + date_property of the retrieval and FIDE ID	
				print("		Setting source - stated in {}.".format(fide_web_item))
				stated_in_claim.setTarget(fide_web_item_page)
				print("		Setting source - retrieved on year {}, month {}, day {}.".format(year_of_retrieval, month_of_retrieval, day_of_retrieval))
				retrieved_on_claim.setTarget(retrieved_on_value)
				print("		Setting source - fide id {}.".format(fide_id))
				fide_id_claim.setTarget(fide_id)
				elo_claim.addSources([stated_in_claim, retrieved_on_claim, fide_id_claim])
				print("Writing to {} is done.\n".format(wd_item))
				found_output_file.write("Item: {}, FIDE ID: {}, Rating: {}.\n".format(wd_item, fide_id, rating))
				claim_counter += 1
			except pywikibot.NoPage:
				print(("{} does not exist. Skipping.\n").format(wd_item))
				continue
print(("Wrote {} claims.").format(claim_counter))
end_time = round(int(time.time() - start_time)/60, 2)
print("Script ran for {} minutes.".format(end_time))
winsound.Beep(2500,700)

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
