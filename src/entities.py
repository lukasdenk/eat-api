# -*- coding: utf-8 -*-

from __future__ import annotations

import datetime
import re
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Set

from src.menu_parser import FMIBistroMenuParser, StudentenwerkMenuParser


class Price:
    base_price: Optional[float]
    price_per_unit: Optional[float]
    unit: Optional[str]

    def __init__(
        self,
        base_price: Optional[float] = None,
        price_per_unit: Optional[float] = None,
        unit: Optional[str] = None,
    ):
        self.base_price = base_price
        self.price_per_unit = price_per_unit
        self.unit = unit

    def __repr__(self):
        if self.price_per_unit and self.unit:
            if isinstance(self.base_price, float):
                return f"{self.base_price:.2f}€ + {self.price_per_unit:.2f} {self.unit}"
            return f"{self.base_price} + {self.price_per_unit} {self.unit}"
        else:
            if isinstance(self.base_price, float):
                return f"{self.base_price:.2f}€"
            return f"{self.base_price}"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return (
                self.base_price == other.base_price
                and self.price_per_unit == other.price_per_unit
                and self.unit == other.unit
            )
        return False

    def to_json_obj(self):
        return {"base_price": self.base_price, "price_per_unit": self.price_per_unit, "unit": self.unit}

    def __hash__(self) -> int:
        # http://stackoverflow.com/questions/4005318/how-to-implement-a-good-hash-function-in-python
        return (hash(self.base_price) << 1) ^ hash(self.price_per_unit) ^ hash(self.unit)


class Prices:
    students: Optional[Price]
    staff: Optional[Price]
    guests: Optional[Price]

    def __init__(self, students: Optional[Price] = None, staff: Optional[Price] = None, guests: Optional[Price] = None):
        self.students = students
        # fall back to the students price if there is only one price available
        if staff is None:
            self.staff = self.students
        else:
            self.staff = staff
        if guests is None:
            self.guests = self.students
        else:
            self.guests = guests

    def setBasePrice(self, base_price: float) -> None:
        if self.students is not None:
            self.students.base_price = base_price
        if self.staff is not None:
            self.staff.base_price = base_price
        if self.guests is not None:
            self.guests.base_price = base_price

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.students == other.students and self.staff == other.staff and self.guests == other.guests
        return False

    def __repr__(self):
        return f"students: {self.students}, staff: {self.staff}, guests: {self.guests}"

    def to_json_obj(self):
        return {
            "students": self.students.to_json_obj() if self.students is not None else None,
            "staff": self.staff.to_json_obj() if self.staff is not None else None,
            "guests": self.guests.to_json_obj() if self.guests is not None else None,
        }

    def __hash__(self) -> int:
        # http://stackoverflow.com/questions/4005318/how-to-implement-a-good-hash-function-in-python
        return hash(self.students) ^ hash(self.staff) ^ hash(self.guests)


class Location:
    def __init__(self, address: str, latitude: float, longitude: float):
        self.address = address
        self.latitude = latitude
        self.longitude = longitude


class Canteen(Enum):
    def __init__(self, location: Location, name: str, url_id: int):
        self.location = location
        self.name = name
        self.url_id = url_id

    MENSA_ARCISSTR = "Mensa Arcisstraße", Location("Arcisstraße 17, München", 48.14742, 11.56722), 421
    MENSA_GARCHING = "Mensa Garching", Location("Boltzmannstraße 19, Garching", 48.268132, 11.672263), 422
    MENSA_LEOPOLDSTR = "Mensa Leopoldstraße", Location("Leopoldstraße 13a, München", 48.156311, 11.582446), 411
    MENSA_LOTHSTR = "Mensa Lothstraße", Location("Lothstraße 13d, München", 48.153989, 11.552424), 431
    MENSA_MARTINSRIED = "Mensa Martinsried", Location("Großhaderner Straße 44, Plategg", 48.109824, 11.460006), 412
    MENSA_PASING = "Mensa Pasing", Location("Am Stadtpark 20, München", 48.141568, 11.451119), 432
    MENSA_WEIHENSTEPHAN = (
        "Mensa Weihenstephan",
        Location(
            "Maximus-von-Imhof-Forum 5, Freising",
            48.39959,
            11.723147,
        ),
        423,
    )
    STUBISTRO_ARCISSTR = "StuBistro Arcisstraße", Location("Leopoldstraße 13A, München", 48.156486, 11.581872), 450
    STUBISTRO_GOETHESTR = "StuBistro Goethestraße", Location("Goethestraße 70, München", 48.131396, 11.558264), 418
    STUBISTRO_GROSSHADERN = (
        "StuBistro Großhadern",
        Location(
            "Butenandtstraße 13, Gebäude F, München",
            48.11363,
            11.46503,
        ),
        414,
    )
    STUBISTRO_ROSENHEIM = "StuBistro Rosenheim", Location("Hochschulstraße 1, Rosenheim", 47.867344, 12.107559), 441
    STUBISTRO_SCHELLINGSTR = (
        "StuBistro Schellingstraße",
        Location(
            "Schellingstraße 3, München",
            48.148893,
            11.579027,
        ),
        416,
    )
    STUCAFE_ADALBERTSTR = "StuCafé Adalbertstraße", Location("Adalbertstraße 5, München", 48.151507, 11.581033), 512
    STUCAFE_AKADEMIE_WEIHENSTEPHAN = (
        "StuCafé Akademie Weihenstephan",
        Location(
            "Alte Akademie 1, Freising",
            48.3948,
            11.729338,
        ),
        526,
    )
    STUCAFE_BOLTZMANNSTR = (
        "StuCafé Boltzmannstraße",
        Location(
            "Boltzmannstraße 15, Garching",
            48.265768,
            11.667593,
        ),
        527,
    )
    STUCAFE_GARCHING = (
        "StuCafé in der Mensa Garching",
        Location(
            "Boltzmannstraße 19, Garching",
            48.268268,
            11.6717,
        ),
        524,
    )
    STUCAFE_KARLSTR = "StuCafé Karlstraße", Location("Karlstraße 6, München", 48.142759, 11.568432), 532
    STUCAFE_PASING = "StuCafé Pasing", Location("Am Stadtpark 20, München", 48.141568, 11.451119), 534
    IPP_BISTRO = "IPP Bistro Garching", Location("Boltzmannstraße 2, 85748 Garching", 48.262371, 11.672702), None
    FMI_BISTRO = "FMI Bistro Garching", Location("Boltzmannstraße 3, 85748 Garching", 48.262408, 11.668028), None
    MEDIZINER_MENSA = "Mediziner Mensa", Location("Ismaninger Straße 22, 81675 München", 48.136569, 11.5993226), None


class Ingredient(Enum):
    _ignore_ = ["studentenwerk_lookup", "fmi_lookup"]

    def __init__(self, german_text: str, studentenwerk_lookup_key: Optional[str], fmi_lookup_key: Optional[str]):
        self.german_text = german_text
        self.studentenwerk_lookup_key = studentenwerk_lookup_key
        self.fmi_lookup_key = fmi_lookup_key

    GLUTEN = "Gluten", None, "a"
    WHEAT = "Weizen", None, "aW"
    RYE = "Roggen", None, "aR"
    BARLEY = "Gerste", None, "aG"
    OAT = "Hafer", None, "aH"
    SPELT = "Dinkel", None, "aD"
    HYBRIDS = "Hybridstämme", None, "aH"
    SHELLFISH = "Krebstiere", None, "b"
    CHICKEN_EGGS = "Eier", None, "c"
    FISH = "Fisch", None, "d"
    PEANUTS = "Erdnüsse", None, "e"
    SOY = "Soja", None, "f"
    MILK = "Milch", None, "g"
    LACTOSE = "Laktose", None, "u"
    ALMONDS = "Mandeln", None, "hMn"
    HAZELNUTS = "Haselnüsse", None, "hH"
    WALNUTS = "Walnüsse", None, "hW"
    CASHEWS = "Cashewnüsse", None, "hK"
    PECAN = "Pekanüsse", None, "hPe"
    PISTACHIOES = "Pistazien", None, "hPi"
    MACADAMIA = "Macadamianüsse", None, "hQ"
    CELERY = "Sellerie", None, "i"
    MUSTARD = "Senf", None, "j"
    SESAME = "Sesam", None, "k"
    SULPHURS = "Schwefeldioxid", None, "l"
    SULFITES = "Sulfite"
    LUPIN = "Lupine", None, "m"
    MOLLUSCS = "Weichtiere", None, "n"
    SHELL_FRUITS = "Schalenfrüchte"

    BAVARIA = "Zertifizierte Qualität Bayern", "GQB", None
    MSC = "Marine Stewardship Council", "MSC", None
    DYESTUFF = "Farbstoffe", "1", None
    PRESERVATIVES = "Preservate", "2", None
    ANTIOXIDANTS = "Antioxidanten"
    FLAVOR_ENHANCER = "Geschmacksverstärker"
    WAXED = "Gewachst"
    PHOSPATES = "Phosphate"
    SWEETENERS = "Süßungsmittel"
    PHENYLALANINE = "Phenylaline"
    COCOA_CONTAINING_GREASE = "Kakaohaltiges Fett"
    GELATIN = "Gelatine"
    ALCOHOL = "Alkohol"
    PORK = "Schweinefleisch"
    BEEF = "Rinderfleisch"
    VEAL = "Kalbsfleisch"
    WILD_MEAT = "Wildfleisch"
    LAMB = "Lammfleisch"
    GARLIC = "Knoblauch"
    POULTRY = "Geflügel"
    CEREAL = "Getreide"

    # if an ingredient is a subclass of another ingredient,
    # the superclass is added in the function lookup. E.g.: A hazelnut is also a shell fruit.
    fmi_lookup: Dict[str, Set[Ingredient]] = {
        "a": {GLUTEN},  # type: ignore
        "aW": {WHEAT},  # type: ignore
        "aR": {RYE},  # type: ignore
        "aG": {BARLEY},  # type: ignore
        "aH": {OAT},  # type: ignore
        "aD": {SPELT},  # type: ignore
        "aHy": {HYBRIDS},  # type: ignore
        "b": {SHELLFISH},  # type: ignore
        "c": {CHICKEN_EGGS},  # type: ignore
        "d": {FISH},  # type: ignore
        "e": {PEANUTS},  # type: ignore
        "f": {SOY},  # type: ignore
        "g": {MILK},  # type: ignore
        "u": {LACTOSE},  # type: ignore
        "h": {SHELL_FRUITS},  # type: ignore
        "hMn": {ALMONDS},  # type: ignore
        "hH": {HAZELNUTS},  # type: ignore
        "hW": {WALNUTS},  # type: ignore
        "hK": {CASHEWS},  # type: ignore
        "hPe": {PECAN},  # type: ignore
        "hPi": {PISTACHIOES},  # type: ignore
        "hQ": {MACADAMIA},  # type: ignore
        "i": {CELERY},  # type: ignore
        "j": {MUSTARD},  # type: ignore
        "k": {SESAME},  # type: ignore
        "l": {SULFITES, SULPHURS},  # type: ignore
        "m": {LUPIN},  # type: ignore
        "n": {MOLLUSCS},  # type: ignore
    }

    studentenwerk_lookup: Dict[str, Set[Ingredient]] = {
        "GQB": {BAVARIA},  # type: ignore
        "MSC": {MSC},  # type: ignore
        "1": {DYESTUFF},  # type: ignore
        "2": {PRESERVATIVES},  # type: ignore
        "3": {ANTIOXIDANTS},  # type: ignore
        "4": {FLAVOR_ENHANCER},  # type: ignore
        "5": {SULPHURS},  # type: ignore
        "6": {DYESTUFF},  # type: ignore
        "7": {WAXED},  # type: ignore
        "8": {PHOSPATES},  # type: ignore
        "9": {SWEETENERS},  # type: ignore
        "10": {PHENYLALANINE},  # type: ignore
        "11": {SWEETENERS},  # type: ignore
        "13": {COCOA_CONTAINING_GREASE},  # type: ignore
        "14": {GELATIN},  # type: ignore
        "99": {ALCOHOL},  # type: ignore
        # meatless is not an ingredient
        "f": {},  # type: ignore
        # vegan is not an ingredient
        "v": {},  # type: ignore
        "S": {PORK},  # type: ignore
        "R": {BEEF},  # type: ignore
        "K": {VEAL},  # type: ignore
        "Kn": {GARLIC},  # type: ignore
        "Ei": {CHICKEN_EGGS},  # type: ignore
        "En": {PEANUTS},  # type: ignore
        "Fi": {FISH},  # type: ignore
        "Gl": {GLUTEN},  # type: ignore
        "GlW": {WHEAT},  # type: ignore
        "GlR": {RYE},  # type: ignore
        "GlG": {BARLEY},  # type: ignore
        "GlH": {OAT},  # type: ignore
        "GlD": {SPELT},  # type: ignore
        "Kr": {SHELLFISH},  # type: ignore
        "Lu": {LUPIN},  # type: ignore
        "Mi": {MILK, LACTOSE},  # type: ignore
        "Sc": {SHELLFISH},  # type: ignore
        "ScM": {ALMONDS},  # type: ignore
        "ScH": {HAZELNUTS},  # type: ignore
        "ScW": {WALNUTS},  # type: ignore
        "ScC": {CASHEWS},  # type: ignore
        "ScP": {PISTACHIOES},  # type: ignore
        "Se": {SESAME},  # type: ignore
        "Sf": {MUSTARD},  # type: ignore
        "Sl": {CELERY},  # type: ignore
        "So": {SOY},  # type: ignore
        "Sw": {SULPHURS, SULFITES},  # type: ignore
        "Wt": {MOLLUSCS},  # type: ignore
    }

    mediziner_ingredient_lookup: Dict[str, Set[Ingredient]] = {  # type: ignore
        "1": {DYESTUFF},  # type: ignore
        "2": {PRESERVATIVES},  # type: ignore
        "3": {ANTIOXIDANTS},  # type: ignore
        "4": {FLAVOR_ENHANCER},  # type: ignore
        "5": {SULPHURS},  # type: ignore
        "6": {DYESTUFF},  # type: ignore
        "7": {WAXED},  # type: ignore
        "8": {PHOSPATES},  # type: ignore
        "9": {SWEETENERS},  # type: ignore
        "A": {ALCOHOL},  # type: ignore
        "B": {GLUTEN},  # type: ignore
        "C": {SHELLFISH},  # type: ignore
        "E": {FISH},  # type: ignore
        "F": {FISH},  # type: ignore
        "G": {POULTRY},  # type: ignore
        "H": {PEANUTS},  # type: ignore
        "K": {VEAL},  # type: ignore
        "L": {LAMB},  # type: ignore
        "M": {SOY},  # type: ignore
        "N": {MILK, LACTOSE},  # type: ignore
        "O": {SHELL_FRUITS},  # type: ignore
        "P": {CELERY},  # type: ignore
        "R": {BEEF},  # type: ignore
        "S": {PORK},  # type: ignore
        "T": {MUSTARD},  # type: ignore
        "U": {SESAME},  # type: ignore
        "V": {SULPHURS, SULFITES},  # type: ignore
        "W": {WILD_MEAT},  # type: ignore
        "X": {LUPIN},  # type: ignore
        "Y": {CHICKEN_EGGS},  # type: ignore
        "Z": {MOLLUSCS},  # type: ignore
    }

    @staticmethod
    def lookup(canteen: Canteen, lookup: str) -> Set[Ingredient]:
        if canteen == Canteen.MEDIZINER_MENSA:
            ingredients: Set[Ingredient] = Ingredient.mediziner_ingredient_lookup.get(lookup, set())  # type: ignore
        elif canteen in StudentenwerkMenuParser.canteens:
            ingredients = Ingredient.studentenwerk_lookup.get(lookup, set())  # type: ignore
        elif canteen in FMIBistroMenuParser.canteens:
            ingredients = Ingredient.fmi_lookup.get(lookup, set())  # type: ignore
        else:
            ingredients = set()

        # insert supertypes
        if ingredients & {
            Ingredient.ALMONDS,
            Ingredient.HAZELNUTS,
            Ingredient.MACADAMIA,
            Ingredient.CASHEWS,
            Ingredient.PECAN,
            Ingredient.PISTACHIOES,
            Ingredient.SESAME,
            Ingredient.WALNUTS,
        }:
            ingredients |= {Ingredient.SHELL_FRUITS}
        if ingredients & {
            Ingredient.BARLEY,
            Ingredient.OAT,
            Ingredient.RYE,
            Ingredient.SPELT,
            Ingredient.WHEAT,
        }:
            ingredients |= {Ingredient.CEREAL}
        return ingredients


class IngredientsOld:
    location: str
    ingredient_set: Set[str]

    ingredient_lookup = {
        "GQB": "Certified Quality - Bavaria",
        "MSC": "Marine Stewardship Council",
        "1": "with dyestuff",
        "2": "with preservative",
        "3": "with antioxidant",
        "4": "with flavor enhancers",
        "5": "sulphured",
        "6": "blackened (olive)",
        "7": "waxed",
        "8": "with phosphate",
        "9": "with sweeteners",
        "10": "contains a source of phenylalanine",
        "11": "with sugar and sweeteners",
        "13": "with cocoa-containing grease",
        "14": "with gelatin",
        "99": "with alcohol",
        "f": "meatless dish",
        "v": "vegan dish",
        "S": "with pork",
        "R": "with beef",
        "K": "with veal",
        "G": "with poultry",  # mediziner mensa
        "W": "with wild meat",  # mediziner mensa
        "L": "with lamb",  # mediziner mensa
        "Kn": "with garlic",
        "Ei": "with chicken egg",
        "En": "with peanut",
        "Fi": "with fish",
        "Gl": "with gluten-containing cereals",
        "GlW": "with wheat",
        "GlR": "with rye",
        "GlG": "with barley",
        "GlH": "with oats",
        "GlD": "with spelt",
        "Kr": "with crustaceans",
        "Lu": "with lupines",
        "Mi": "with milk and lactose",
        "Sc": "with shell fruits",
        "ScM": "with almonds",
        "ScH": "with hazelnuts",
        "ScW": "with Walnuts",
        "ScC": "with cashew nuts",
        "ScP": "with pistachios",
        "Se": "with sesame seeds",
        "Sf": "with mustard",
        "Sl": "with celery",
        "So": "with soy",
        "Sw": "with sulfur dioxide and sulfites",
        "Wt": "with mollusks",
    }
    """A dictionary of all ingredients (from the Studentenwerk) with their description."""

    fmi_ingredient_lookup = {
        "a": "Gluten",
        "aW": "Weizen",
        "aR": "Roggen",
        "aG": "Gerste",
        "aH": "Hafer",
        "aD": "Dinkel",
        "aHy": "Hybridstämme",
        "b": "Krebstiere",
        "c": "Eier",
        "d": "Fisch",
        "e": "Erdnüsse",
        "f": "Soja",
        "g": "Milch",
        "u": "Laktose",
        "h": "Schalenfrüchte",
        "hMn": "Mandeln",
        "hH": "Haselnüsse",
        "hW": "Walnüsse",
        "hK": "Cashewnüsse",
        "hPe": "Pekanüsse",
        "hPi": "Pistazien",
        "hQ": "Macadamianüsse",
        "i": "Sellerie",
        "j": "Senf",
        "k": "Sesam",
        "l": "Schwefeldioxid und Sulphite",
        "m": "Lupine",
        "n": "Weichtiere",
    }

    mediziner_ingredient_lookup = {
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "A": "99",
        "B": "Gl",
        "C": "Kr",
        "E": "Fi",
        "F": "Fi",
        "G": "G",
        "H": "En",
        "K": "K",
        "L": "L",
        "M": "So",
        "N": "Mi",
        "O": "Sc",
        "P": "Sl",
        "R": "R",
        "S": "S",
        "T": "Sf",
        "U": "Se",
        "V": "Sw",
        "W": "W",
        "X": "Lu",
        "Y": "Ei",
        "Z": "Wt",
    }

    def __init__(self, location: str):
        self.location = location
        self.ingredient_set = set()

    def _values_lookup(self, values: Sequence[str], lookup: Optional[Dict[str, str]]) -> None:
        """
        Normalizes ingredients to the self.ingredient_lookup codes.

        Args:
            values: A sequence of ingredients codes.
            lookup: If needed, a mapping from a canteen specific ingredients codes to the self.ingredient_lookup codes.
        """
        for value in values:
            # ignore empty values
            if not value or value.isspace():
                continue
            if (not lookup and value not in self.ingredient_lookup) or (lookup and value not in lookup):

                # sometimes the ‘,’ is missing between the ingredients (especially with IPP) and we try to split again
                # with capital letters.
                split_values: List[Any] = re.findall(r"[a-züöäA-ZÜÖÄ][^A-ZÜÖÄ]*", value)
                if split_values:
                    self._values_lookup(split_values, lookup)
                    continue
                else:
                    print("Unknown ingredient for " + self.location + " found: " + str(value))
                    continue

            if lookup:
                self.ingredient_set.add(lookup[value])
            else:
                self.ingredient_set.add(value)

    def parse_ingredients(self, values: str) -> None:
        """
        Parse and creates a normalized list of ingredients.

        Args:
            values: String with comma separated ingredients codes.
        """
        values = values.strip()
        split_values: List[str] = values.split(",")
        # check for special parser/ingredient translation required
        if self.location == "fmi-bistro":
            self._values_lookup(split_values, self.fmi_ingredient_lookup)
        elif self.location == "mediziner-mensa":
            self._values_lookup(split_values, self.mediziner_ingredient_lookup)
        # default to the "Studentenwerk" ingredients
        # "ipp-bistro" also uses the "Studentenwerk" ingredients since all
        # dishes contain the same ingredients
        else:
            self._values_lookup(split_values, None)

    def __hash__(self) -> int:
        return hash(frozenset(self.ingredient_set))


class Dish:
    name: str
    prices: Prices
    ingredients: Set[str]
    dish_type: str

    def __init__(self, name: str, prices: Prices, ingredients: Set[str], dish_type: str):
        self.name = name
        self.prices = prices
        self.ingredients = ingredients
        self.dish_type = dish_type

    def __repr__(self):
        return f"{self.name} {str(sorted(self.ingredients))}: {str(self.prices)}"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return (
                self.name == other.name
                and self.prices == other.prices
                and self.ingredients == other.ingredients
                and self.dish_type == other.dish_type
            )
        return False

    def to_json_obj(self):
        return {
            "name": self.name,
            "prices": self.prices.to_json_obj(),
            "ingredients": sorted(self.ingredients),
            "dish_type": self.dish_type,
        }

    def __hash__(self) -> int:
        # http://stackoverflow.com/questions/4005318/how-to-implement-a-good-hash-function-in-python
        return (hash(self.name) << 1) ^ hash(self.prices) ^ hash(frozenset(self.ingredients)) ^ hash(self.dish_type)


class Menu:
    menu_date: datetime.date
    dishes: List[Dish]

    def __init__(self, menu_date: datetime.date, dishes: List[Dish]):
        self.menu_date = menu_date
        self.dishes = dishes

    def __repr__(self):
        return str(self.menu_date) + ": " + str(self.dishes)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            dishes_equal = set(self.dishes) == set(other.dishes)
            date_equal = self.menu_date == other.menu_date
            return dishes_equal and date_equal
        return False

    def remove_duplicates(self):
        unique: List[Dish] = []
        seen: Set[Dish] = set()

        for dish in self.dishes:
            if dish not in seen:
                unique.append(dish)
                seen.add(dish)

        self.dishes = unique


class Week:
    calendar_week: int
    year: int
    days: List[Menu]

    def __init__(self, calendar_week: int, year: int, days: List[Menu]):
        self.calendar_week = calendar_week
        self.year = year
        self.days = days

    def __repr__(self):
        week_str = f"Week {self.year}-{self.calendar_week}"
        for day in self.days:
            week_str += f"\n {day}"
        return week_str

    def to_json_obj(self):
        return {
            "number": self.calendar_week,
            "year": self.year,
            "days": [
                {"date": str(menu.menu_date), "dishes": [dish.to_json_obj() for dish in menu.dishes]}
                for menu in self.days
            ],
        }

    @staticmethod
    # def to_weeks(menus: Dict[datetime.date, Menu]) -> Dict[int, Week]:
    def to_weeks(menus):
        weeks: Dict[int, Week] = {}
        for menu_key in menus:
            menu: Menu = menus[menu_key]
            menu_date = menu.menu_date
            # get calendar week
            calendar_week = menu_date.isocalendar()[1]
            # get year of the calendar week. watch out that for instance jan 01 can still be in week 52 of the
            # previous year
            year_of_calendar_week = (
                menu_date.year - 1 if calendar_week == 52 and menu_date.month == 1 else menu_date.year
            )

            # append menus to respective week
            week: Week = weeks.get(calendar_week, Week(calendar_week, year_of_calendar_week, []))
            week.days.append(menu)
            weeks[calendar_week] = week
        return weeks

    @staticmethod
    def get_non_weekend_days_for_calendar_week(year: int, calendar_week: int) -> List[datetime.date]:
        days = []

        start_date = datetime.date.fromisocalendar(year, calendar_week, 1)
        for _ in range(5):
            days += [start_date]
            start_date += datetime.timedelta(days=1)
        return days
