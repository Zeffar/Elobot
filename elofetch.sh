#!/bin/bash
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
  printf "Usage: elofetch.sh date\n"
  printf "Example: elofetch.sh jan12 for January 2018 ratings.\n"
  printf "Before running date retrieved and date of rating inside MUST be updated.\n"
  exit 0
fi

printf "Script fetches ratings of FIDE registered players and outputs QuickStatements batch.\n"
printf "Before running date retrieved and date of rating inside wd-triplets-quiet.py MUST be updated.\n"

printf "Did you update wd-triplets-quiet.py (y/n)? "
read answer
if [ "$answer" != "${answer#[Yy]}" ]; then
  printf "Fetching file from ratings.fide.com.\n"
  wget -q http://ratings.fide.com/download/standard_"$1"frl_xml.zip
  unzip -q standard_"$1"frl_xml.zip

  printf "Extracting data.\n"
  xmlstarlet sel -t -m "//fideid" -v . -n standard_"$1"frl_xml.xml > ids.txt
  xmlstarlet sel -t -m "//rating" -v . -n standard_"$1"frl_xml.xml > ratings.txt
  paste -d , ids.txt ratings.txt > pairs.csv
  python3 wd-triplets-quiet.py

  printf "Cleaning up.\n"
  rm pairs.csv ids.txt ratings.txt standard_"$1"frl_xml.zip standard_"$1"frl_xml.xml

  printf "Output can be found at elo-item-rating-triplet.csv and item-fide-id-match-not-found.csv\n"
else
  exit 0
fi
