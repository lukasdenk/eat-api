import os.path
import sys

import entities
from utils import file_util


def update_canteens(base_dir: str = "") -> None:
    file_util.write_json(os.path.join(base_dir, "locations.json"), list(entities.Location))


def update_ingredients(base_dir: str = "") -> None:
    file_util.write_json(os.path.join(base_dir, "ingredients.json"), list(entities.Ingredient))


def update_diets(base_dir: str = "") -> None:
    file_util.write_json(os.path.join(base_dir, "diets.json"), list(entities.Diet))


if __name__ == "__main__":
    base_directory = ""
    if len(sys.argv) > 1:
        base_directory = sys.argv[1]
    update_canteens(base_directory)
    update_ingredients(base_directory)
    update_diets(base_directory)
