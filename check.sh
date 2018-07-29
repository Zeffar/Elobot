#!/bin/bash
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
  printf "Check for data accuracy before claiming to wikidata.\n"
  printf "Usage: check.sh jun18 706035 for checking record of player with from June 2018 with FIDE ID 706035.\n"
  exit 0
fi

printf "Check for data accuracy before claiming to wikidata. Run check.sh -h for help.\n"
wget -q http://ratings.fide.com/download/standard_$1frl_xml.zip
unzip -q standard_$1frl_xml.zip
rm standard_$1frl_xml.zip

printf "___________________________\n"
grep -A 8 $2 standard_$1frl_xml.xml
printf "___________________________\n\n"
printf "XML file preserved, for recheck run grep -A 8 FIDE_ID standard_$1frl_xml.xml\n"
