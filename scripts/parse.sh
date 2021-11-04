#!/bin/bash

LOC_LIST=( "mensa-arcisstr" "mensa-garching" "mensa-leopoldstr" "mensa-lothstr" \
"mensa-martinsried" "mensa-pasing" "mensa-weihenstephan" "stubistro-arcisstr" "stubistro-goethestr" \
"stubistro-grosshadern" "stubistro-rosenheim" "stubistro-schellingstr" "stucafe-adalbertstr" \
"stucafe-akademie-weihenstephan" "stucafe-boltzmannstr" "stucafe-garching" "stucafe-karlstr" "stucafe-pasing" \
"ipp-bistro" "fmi-bistro" "mediziner-mensa" )
OUT_DIR="${OUT_DIR:-dist}"
LANGUAGE="${LANGUAGE_EAT_API:-de}"

# Delete old output directory if it exists:
if [ -d $OUT_DIR ]; then
		rm -r $OUT_DIR
fi
# Create empty output directory:
mkdir $OUT_DIR

# Parse all canteens:
for loc in "${LOC_LIST[@]}"; do
    echo "Parsing menus for: " "$loc"
    python3 src/main.py -p "$loc" -j "./$OUT_DIR/$loc" -c --language "$LANGUAGE"
done

# Combine all combined.json files to one all.json file:
python3 scripts/combine.py
# Remove all dishes which are older than one day
# and reorganize them in a more efficient format:
python3 scripts/reformat.py

# Copy canteens.json in the output directory:
echo "Coppying canteens..."
cp src/canteens.json $OUT_DIR
echo "Done"

openmensa_list=( "ipp-bistro" "fmi-bistro" )

for loc in "${openmensa_list[@]}"; do
    echo "Parsing openmensa menus for: " "$loc"
    python3 src/main.py -p "$loc" --openmensa "./dist/$loc"
done

tree dist/
