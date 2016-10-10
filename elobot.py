import pywikibot
import re
import json
import urllib.parse
import requests
import time
import winsound
import os

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

date_property = "P585"
date_claim = pywikibot.Claim(repo, date_property)
stated_in_property = "P248"
stated_in_claim = pywikibot.Claim(repo, stated_in_property)
retrieved_on_property = "P813"
retrieved_on_claim = pywikibot.Claim(repo, retrieved_on_property)
fide_web_item = "Q27038151"
fide_web_item_page = pywikibot.ItemPage(repo, fide_web_item)
elo_property = "P1087"
elo_claim = pywikibot.Claim(repo, elo_property)
fide_id_property = "P1440"
fide_id_claim = pywikibot.Claim(repo, fide_id_property)
repeat = "y"
exception_counter = 0
claim_counter = 1
start_time = time.time()


def clear():
    os.system('cls')


def elobot():
    global exception_counter, claim_counter
    input_csv_file = input("Give the name of the input csv file: ")  # for example "standard_apr14.csv"
    print("The following values must match the input csv file given above!\n")
    time.sleep(2)
    year_of_rating = int(
        input("Give the year of the rating: "))  # for ex "2014"
    month_of_rating = int(input("Give the month of the rating: "))  # for ex "4" for April
    year_of_retrieval = int(
        input("Give the year of the retrieval: "))  # for ex "2016"
    month_of_retrieval = int(
        input("Give the month of the retrieval: "))  # for ex "9"
    day_of_retrieval = int(
        input("Give the day of the retrieval: "))  # for ex "21"
    date_value = pywikibot.WbTime(year=year_of_rating, month=month_of_rating)
    retrieved_on_value = pywikibot.WbTime(
        year=year_of_retrieval, month=month_of_retrieval, day=day_of_retrieval)
# open external files
    with open(input_csv_file, "r", encoding="utf-8") as fide_csv_rating_file, \
            open("chess-elo-item-rating-output.txt", "w", encoding="utf-8") as found_output_file, \
            open("chess-didntfind-fideid-output.txt", "w", encoding="utf-8") as didnt_find_output_file:
        # query wd, output in json
        print("\nInput file: {}\nEloBot is going to check and possibly write claims with these values:"
              "\n    qualifier: date (P585) - year {}, month {}"
              "\n    source:\n        retrieved (P813) - year {}, month {}, day {}"
              "\n        player's own FIDE ID ({})"
              "\n        stated in ({}) - ratings.fide.com ({})".format(input_csv_file, year_of_rating,
                                                                        month_of_rating, year_of_retrieval,
                                                                        month_of_retrieval, day_of_retrieval, fide_id_property,
                                                                        stated_in_property, fide_web_item))
        input("\nIf the above statements are correct, press Enter to start.\n")
        query_string = """SELECT ?item ?value WHERE {?item wdt:P1440 ?value .}"""
        wd_query = urllib.parse.quote(query_string)
        wd_query_url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query={}&format=json".format(
            wd_query)
        url = requests.get(wd_query_url)
        json_data = json.loads(url.text)
        item_list = [[data["item"]["value"].replace("http://www.wikidata.org/entity/", ""),
                      data["value"]["value"]] for data in json_data["results"]["bindings"]]
# parse csv input
        fide_rating_file = fide_csv_rating_file.read()
        fide_rating_file = fide_rating_file.split("\n")
        fide_rating_file2 = [f for f in fide_rating_file if len(f) > 0]
        fide_rating_file3 = [f.split(",") for f in fide_rating_file2]
        fide_ratings = {f[0]: f[1] for f in fide_rating_file3}
# write to wd
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
                            print("Checking elo claim of the item {}."
                                  "\nThis claim HAS a qualifier date - year {}, month {}.\n".format(wd_item, year_of_rating,
                                                                                                    month_of_rating))
                            break
                if has_claim_with_this_date:
                    print("Checking elo claim of the item {}."
                          "\nThis claim does NOT have a qualifier date - year {}, month {}.\n".format(wd_item, year_of_rating,
                                                                                                      month_of_rating))
                    continue
                if fide_id not in fide_ratings:
                    print(("FIDE ID {} for item {} returned by the query was NOT found in the input file.\n").format(
                        fide_id, wd_item))
                    didnt_find_output_file.write(
                        ("Item:{}, FIDE ID:{}\n").format(wd_item, fide_id))
                    continue
                rating = int(fide_ratings[fide_id])
# write claims
                print("Writing statement number: {}".format(claim_counter))
                print("Setting P1087 claim to {}, value of {}.".format(
                    wd_item, rating))
                elo_claim.setTarget(pywikibot.WbQuantity(rating))
                player_item.addClaim(elo_claim)
# write qualifier - date
                print(
                    "    Setting qualifier - date: year {}, month {}.".format(year_of_rating, month_of_rating))
                date_claim.setTarget(date_value)
                elo_claim.addQualifier(date_claim)
# write sources - stated in + date_property of the retrieval and FIDE ID
                print("        Setting source - stated in {}.".format(fide_web_item))
                stated_in_claim.setTarget(fide_web_item_page)
                print("        Setting source - retrieved on year {}, month {}, day {}.".format(year_of_retrieval,
                                                                                                month_of_retrieval,
                                                                                                day_of_retrieval))
                retrieved_on_claim.setTarget(retrieved_on_value)
                print("        Setting source - FIDE ID {}.".format(fide_id))
                fide_id_claim.setTarget(fide_id)
                elo_claim.addSources(
                    [stated_in_claim, retrieved_on_claim, fide_id_claim])
                print("Writing to {} is done.\n".format(wd_item))
                found_output_file.write(
                    "Item: {}, FIDE ID: {}, Rating: {}.\n".format(wd_item, fide_id, rating))
                claim_counter += 1
            except pywikibot.NoPage:
                print(("{} does not exist. Skipping.\n").format(wd_item))
                winsound.Beep(2500, 200)
                exception_counter += 1
                time.sleep(5)
                continue
            except pywikibot.data.api.APIError:
                print("Wikidata is probably in readonly mode. Waiting 5 minutes before continuing.")
                winsound.Beep(2500, 200)
                exception_counter += 1
                time.sleep(300)
                continue
            except:
                print("Unspecified exception caught. Waiting 60 seconds before continuing.")
                winsound.Beep(2500, 200)
                exception_counter += 1
                time.sleep(60)
                continue
# run elobot
print("EloBot is a script for writing elo rating claims to Wikidata - a collaboratively edited knowledge base "
      "operated by the Wikimedia Foundation.\n")
time.sleep(2)
while repeat == "y":
    elobot()
    total_runtime = round(int(time.time() - start_time) / 60)
    print("EloBot ran for {} minutes and wrote {} claims.".format(
        total_runtime, claim_counter))
    print("Total number of exceptions: {}".format(exception_counter))
    winsound.Beep(2500, 500)
    repeat = input("Would you like to run EloBot again? Press \"y\" for repeating.")
    clear()

# Calendar:
#    jan    1
#    feb    2
#    mar    3
#    apr    4
#    may    5
#    jun    6
#    jul    7
#    aug    8
#    sep    9
#    oct    10
#    nov    11
#    dec    12
# Properties:
#    property P813 "retrieved", to be found at https://www.wikidata.org/wiki/Property:P813
#    property P248 "stated in", to be found at https://www.wikidata.org/wiki/Property:P248
#    property P585 "date_property" to be found at https://www.wikidata.org/wiki/Property:P585
#    property P1087 "elo" to be found at https://www.wikidata.org/wiki/Property:1087
#    property P1440 "FIDE ID", to be found at https://www.wikidata.org/wiki/Property:P1440
#    item "ratings.fide.com" to be found at https://www.wikidata.org/wiki/Q27038151
# Deleted items:
#    Q11814034 - Dziubinski,id 1126385, https://ratings.fide.com/card.phtml?event=1126385
