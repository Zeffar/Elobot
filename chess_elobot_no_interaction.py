import json
import time
import urllib.parse

import pywikibot as pwb
import requests

site = pwb.Site("wikidata", "wikidata")
repo = site.data_repository()
date_property = "P585"
date_claim = pwb.Claim(repo, date_property)
stated_in_property = "P248"
stated_in_claim = pwb.Claim(repo, stated_in_property)
retrieved_on_property = "P813"
retrieved_on_claim = pwb.Claim(repo, retrieved_on_property)
fide_web_item = "Q27038151"
fide_web_item_page = pwb.ItemPage(repo, fide_web_item)
elo_property = "P1087"
elo_claim = pwb.Claim(repo, elo_property)
fide_id_property = "P1440"
fide_id_claim = pwb.Claim(repo, fide_id_property)


def elobot(input_csv_file, year_of_rating, month_of_rating, year_of_retrieval, month_of_retrieval, day_of_retrieval):
    with open(input_csv_file, "r", encoding="utf-8") as fide_csv_rating_file, \
            open("chess-elo-item-rating-output.txt", "w", encoding="utf-8") as found_output_file, \
            open("chess-didnt-find-fideid-output.txt", "w", encoding="utf-8") as didnt_find_output_file:
        date_value = pwb.WbTime(year=year_of_rating, month=month_of_rating)
        retrieved_on_value = pwb.WbTime(year=year_of_retrieval, month=month_of_retrieval, day=day_of_retrieval)
        query_string = """SELECT ?item ?value WHERE {?item wdt:P1440 ?value .}"""
        wd_query = urllib.parse.quote(query_string)
        wd_query_url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query={}&format=json".format(wd_query)
        url = requests.get(wd_query_url)
        json_data = json.loads(url.text)
        item_list = [[data["item"]["value"].replace("http://www.wikidata.org/entity/", ""),
                      data["value"]["value"]] for data in json_data["results"]["bindings"]]
        fide_rating_file = fide_csv_rating_file.read()
        fide_rating_file = fide_rating_file.split("\n")
        fide_rating_file2 = [f for f in fide_rating_file if len(f) > 0]
        fide_rating_file3 = [f.split(",") for f in fide_rating_file2]
        fide_ratings = {f[0]: f[1] for f in fide_rating_file3}
        for player in item_list:
            has_claim_with_this_date = False
            wd_item = player[0]
            fide_id = player[1]
            player_item = pwb.ItemPage(repo, wd_item)
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
                    didnt_find_output_file.write("Item:{}, FIDE ID:{}\n".format(wd_item, fide_id))
                    continue
                rating = int(fide_ratings[fide_id])
                elo_claim.setTarget(pwb.WbQuantity(rating))
                player_item.addClaim(elo_claim)
                date_claim.setTarget(date_value)
                elo_claim.addQualifier(date_claim)
                stated_in_claim.setTarget(fide_web_item_page)
                retrieved_on_claim.setTarget(retrieved_on_value)
                fide_id_claim.setTarget(fide_id)
                elo_claim.addSources([stated_in_claim, retrieved_on_claim, fide_id_claim])
                found_output_file.write("Item: {}, FIDE ID: {}, Rating: {}.\n".format(wd_item, fide_id, rating))
            except pwb.NoPage:
                continue
            except pwb.data.api.APIError:
                time.sleep(300)
                continue
            except:
                time.sleep(300)
                continue


elobot(input_csv_file="csv/standard_jan13.csv", year_of_rating=2013, month_of_rating=1,
       year_of_retrieval=2016, month_of_retrieval=9, day_of_retrieval=21)  # example
