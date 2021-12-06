#!/bin/bash

CANTEEN_LIST=( "mensa-arcisstr" "mensa-garching" "mensa-leopoldstr" "mensa-lothstr" \
"mensa-martinsried" "mensa-pasing" "mensa-weihenstephan" "stubistro-arcisstr" "stubistro-goethestr" \
"stubistro-grosshadern" "stubistro-rosenheim" "stubistro-schellingstr" "stucafe-adalbertstr" \
"stucafe-akademie-weihenstephan" "stucafe-boltzmannstr" "stucafe-garching" "stucafe-karlstr" "stucafe-pasing" \
"ipp-bistro" "fmi-bistro" "mediziner-mensa" )
OUT_DIR="${OUT_DIR:-dist}"
LANGUAGE="${LANGUAGE_EAT_API:-DE}"

# Delete old output directory if it exists:
if [ -d $OUT_DIR ]; then
		rm -r $OUT_DIR
fi
# Create empty output directory:
mkdir -p $OUT_DIR

# Copy canteens.json in the output directory:
echo "Copying canteens..."
cp src/canteens.json $OUT_DIR
echo "Done"

# Parse all canteens:
for canteen in "${CANTEEN_LIST[@]}"; do
    echo "Parsing menus for: " "$canteen"
    python3 src/main.py -p "$canteen" -j "./$OUT_DIR/$canteen" -c
done

# Combine all combined.json files to one all.json file:
python3 scripts/combine.py
# Remove all dishes which are older than one day
# and reorganize them in a more efficient format:
python3 scripts/reformat.py

openmensa_list=( "ipp-bistro" "fmi-bistro" )

for CANTEEN in "${openmensa_list[@]}"; do
    echo "Parsing openmensa menus for: " "$CANTEEN"
    python3 src/main.py -p "$CANTEEN" --openmensa "$OUT_DIR/$CANTEEN"
done

ENUM_JSON_PATH="$OUT_DIR/enums"
mkdir -p "$ENUM_JSON_PATH"
echo "Creating Canteen-, Language- and Label-Enum"
python3 ./src/enum_json_creator.py "$ENUM_JSON_PATH"

tree "$OUT_DIR"
