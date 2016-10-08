import pywikibot, re, json, urllib.parse, requests, time
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
input_csv_file = 
year_of_rating = 
month_of_rating = 
year_of_retrieval = 
month_of_retrieval = 
day_of_retrieval = 
date_property = "P585"
date_value = pywikibot.WbTime(year = year_of_rating, month = month_of_rating)
date_claim = pywikibot.Claim(repo, date_property)
stated_in_property = "P248"
stated_in_claim = pywikibot.Claim(repo, stated_in_property)
retrieved_on_property = "P813"
retrieved_on_value = pywikibot.WbTime(year = year_of_retrieval, month = month_of_retrieval, day = day_of_retrieval)
retrieved_on_claim = pywikibot.Claim(repo, retrieved_on_property)
fide_web_item = "Q27038151"
fide_web_item_page = pywikibot.ItemPage(repo, fide_web_item)
elo_property = "P1087"
elo_claim = pywikibot.Claim(repo, elo_property)
fide_id_property = "P1440"
fide_id_claim = pywikibot.Claim(repo, fide_id_property)
with open(input_csv_file, "r", encoding="utf-8") as fide_csv_rating_file, \
open("chess-elo-item-rating-output.txt", "w", encoding = "utf-8") as  found_output_file, \
open("chess-didntfind-fideid-output.txt", "w", encoding = "utf-8") as didnt_find_output_file:
    query_string = """SELECT ?item ?value WHERE {?item wdt:P1440 ?value .}"""
    wd_query = urllib.parse.quote(query_string)
    wd_query_url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query={}&format=json".format(wd_query)
    url = requests.get(wd_query_url)
    json_data = json.loads(url.text)
    item_list = [[data["item"]["value"].replace("http://www.wikidata.org/entity/", ""),
                data["value"]["value"]] for data in json_data["results"]["bindings"]]
    fide_rating_file = fide_csv_rating_file.read()
    fide_rating_file = fide_rating_file.split("\n")
    fide_rating_file2 = [f for f in fide_rating_file if len(f)>0]
    fide_rating_file3 = [f.split(",") for f in fide_rating_file2]
    fide_ratings = {f[0]:f[1] for f in fide_rating_file3}
    claim_counter = 1
    for player in item_list:
        has_claim_with_this_date = False
        wd_item = player[0]
        fide_id = player[1]
        player_item = pywikibot.ItemPage(repo, wd_item)
        try:
            player_item.get()
            for claim in player_item.claims.get(elo_property, []):
                for qualifier in claim.qualifiers.get(date_property, []):
                        if qualifier.target_equals(date_value):
                            has_claim_with_this_date = True
                            break
            if has_claim_with_this_date:
                continue
            if fide_id not in fide_ratings:
                didnt_find_output_file.write(("Item:{}, FIDE ID:{}\n").format(wd_item,fide_id))
                continue
            rating = int(fide_ratings[fide_id])
            elo_claim.setTarget(pywikibot.WbQuantity(rating))
            player_item.addClaim(elo_claim)
            date_claim.setTarget(date_value)
            elo_claim.addQualifier(date_claim)
            stated_in_claim.setTarget(fide_web_item_page)
            retrieved_on_claim.setTarget(retrieved_on_value)
            fide_id_claim.setTarget(fide_id)
            elo_claim.addSources([stated_in_claim, retrieved_on_claim, fide_id_claim])
            found_output_file.write("Item: {}, FIDE ID: {}, Rating: {}.\n".format(wd_item, fide_id, rating))
        except pywikibot.NoPage:
            time.sleep(30)
            continue
        except pywikibot.data.api.APIError:
            time.sleep(300)
            continue
        except:
            time.sleep(60)
            continue
