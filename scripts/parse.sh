#!/bin/bash

CANTEEN_LIST=( "MENSA_ARCISSTR" "MENSA_GARCHING" "MENSA_LEOPOLDSTR" "MENSA_LOTHSTR" "MENSA_MARTINSRIED" \
"MENSA_PASING" "MENSA_WEIHENSTEPHAN" "STUBISTRO_ARCISSTR" "STUBISTRO_GOETHESTR" \
"STUBISTRO_GROSSHADERN" "STUBISTRO_ROSENHEIM" "STUBISTRO_SCHELLINGSTR" "STUCAFE_ADALBERTSTR" \
"STUCAFE_AKADEMIE_WEIHENSTEPHAN" "STUCAFE_BOLTZMANNSTR" "STUCAFE_GARCHING" "STUCAFE_KARLSTR" \
"STUCAFE_PASING" "IPP_BISTRO" "FMI_BISTRO" "MEDIZINER_MENSA" )
OUT_DIR="${OUT_DIR:-dist}"
LANGUAGE="${LANGUAGE_EAT_API:-DE}"

# Delete old output directory if it exists:
if [ -d $OUT_DIR ]; then
		rm -r $OUT_DIR
fi
# Create empty output directory:
mkdir -p $OUT_DIR

parse(){
    echo "Parsing menus for: $1 in $2..."
    python3 src/main.py -p "$1" -j "./$OUT_DIR/$1" -c
    echo "Parsing menus for: $1 done."
}

# Parse all canteens:
for canteen in "${CANTEEN_LIST[@]}";
do
( parse $canteen $LANGUAGE ) &
done
wait # Wait for all processes to finish

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

# Copy canteens.json in the output directory (for backwards compatibility):
echo "Copying canteens..."
cp "$ENUM_JSON_PATH/canteens.json" $OUT_DIR
echo "Done"

tree "$OUT_DIR"
