# -*- coding: utf-8 -*-

# Postponed Evaluation of Annotations to allow using a class inside a class for annotations
from __future__ import annotations

import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set


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

    def set_base_price(self, base_price: float) -> None:
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


class Site:
    def __init__(self, address: str, latitude: float, longitude: float):
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def to_json_obj(self):
        return {
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }


class Location(Enum):
    # Some of the locations do not use the general Studentenwerk system and therefore do not have a url_id.
    def __init__(self, long_name: str, site: Site, url_id: int):
        self.long_name = long_name
        self.site = site
        self.url_id = url_id
        self.directory_format = self.name.lower().replace("_", "-")

    MENSA_ARCISSTR = "Mensa Arcisstraße", Site("Arcisstraße 17, München", 48.14742, 11.56722), 421
    MENSA_GARCHING = "Mensa Garching", Site("Boltzmannstraße 19, Garching", 48.268132, 11.672263), 422
    MENSA_LEOPOLDSTR = "Mensa Leopoldstraße", Site("Leopoldstraße 13a, München", 48.156311, 11.582446), 411
    MENSA_LOTHSTR = "Mensa Lothstraße", Site("Lothstraße 13d, München", 48.153989, 11.552424), 431
    MENSA_MARTINSRIED = "Mensa Martinsried", Site("Großhaderner Straße 44, Plategg", 48.109824, 11.460006), 412
    MENSA_PASING = "Mensa Pasing", Site("Am Stadtpark 20, München", 48.141568, 11.451119), 432
    MENSA_WEIHENSTEPHAN = (
        "Mensa Weihenstephan",
        Site(
            "Maximus-von-Imhof-Forum 5, Freising",
            48.39959,
            11.723147,
        ),
        423,
    )
    STUBISTRO_ARCISSTR = "StuBistro Arcisstraße", Site("Leopoldstraße 13A, München", 48.156486, 11.581872), 450
    STUBISTRO_GOETHESTR = "StuBistro Goethestraße", Site("Goethestraße 70, München", 48.131396, 11.558264), 418
    STUBISTRO_GROSSHADERN = (
        "StuBistro Großhadern",
        Site(
            "Butenandtstraße 13, Gebäude F, München",
            48.11363,
            11.46503,
        ),
        414,
    )
    STUBISTRO_ROSENHEIM = "StuBistro Rosenheim", Site("Hochschulstraße 1, Rosenheim", 47.867344, 12.107559), 441
    STUBISTRO_SCHELLINGSTR = (
        "StuBistro Schellingstraße",
        Site(
            "Schellingstraße 3, München",
            48.148893,
            11.579027,
        ),
        416,
    )
    STUCAFE_ADALBERTSTR = "StuCafé Adalbertstraße", Site("Adalbertstraße 5, München", 48.151507, 11.581033), 512
    STUCAFE_AKADEMIE_WEIHENSTEPHAN = (
        "StuCafé Akademie Weihenstephan",
        Site(
            "Alte Akademie 1, Freising",
            48.3948,
            11.729338,
        ),
        526,
    )
    STUCAFE_BOLTZMANNSTR = (
        "StuCafé Boltzmannstraße",
        Site(
            "Boltzmannstraße 15, Garching",
            48.265768,
            11.667593,
        ),
        527,
    )
    STUCAFE_GARCHING = (
        "StuCafé in der Mensa Garching",
        Site(
            "Boltzmannstraße 19, Garching",
            48.268268,
            11.6717,
        ),
        524,
    )
    STUCAFE_KARLSTR = "StuCafé Karlstraße", Site("Karlstraße 6, München", 48.142759, 11.568432), 532
    STUCAFE_PASING = "StuCafé Pasing", Site("Am Stadtpark 20, München", 48.141568, 11.451119), 534
    IPP_BISTRO = "IPP Bistro Garching", Site("Boltzmannstraße 2, 85748 Garching", 48.262371, 11.672702), None
    FMI_BISTRO = "FMI Bistro Garching", Site("Boltzmannstraße 3, 85748 Garching", 48.262408, 11.668028), None
    MEDIZINER_MENSA = "Mediziner Mensa", Site("Ismaninger Straße 22, 81675 München", 48.136569, 11.5993226), None

    @staticmethod
    def get_location_by_str(location_str: str) -> Location:
        return Location[location_str.upper().replace("-", "_")]

    def to_json_obj(self):
        return {
            "name": self.name,
            "long_name": self.long_name,
            "site": self.site.to_json_obj(),
            "url_id": self.url_id,
        }


class Diet(Enum):
    VEGAN = auto()
    VEGETARIAN = auto()
    CARNIVOROUS = auto()
    PESCETARIAN = auto()

    def to_json_obj(self):
        return {
            "name": self.name,
        }


class Ingredient(Enum):
    # mypy does not recognize that studentenwerk_lookup, fmi_lookup and mediziner_lookup are not Enum types.
    # This is the reason for the many "# type: ignore" comments.
    _ignore_ = ["studentenwerk_lookup", "fmi_lookup", "mediziner_lookup"]

    def __init__(self, german_text: str):
        self.german_text = german_text

    GLUTEN = "Gluten"
    WHEAT = "Weizen"
    RYE = "Roggen"
    BARLEY = "Gerste"
    OAT = "Hafer"
    SPELT = "Dinkel"
    HYBRIDS = "Hybridstämme"
    SHELLFISH = "Krebstiere"
    CHICKEN_EGGS = "Eier"
    FISH = "Fisch"
    PEANUTS = "Erdnüsse"
    SOY = "Soja"
    MILK = "Milch"
    LACTOSE = "Laktose"
    ALMONDS = "Mandeln"
    HAZELNUTS = "Haselnüsse"
    WALNUTS = "Walnüsse"
    CASHEWS = "Cashewnüsse"
    PECAN = "Pekanüsse"
    PISTACHIOES = "Pistazien"
    MACADAMIA = "Macadamianüsse"
    CELERY = "Sellerie"
    MUSTARD = "Senf"
    SESAME = "Sesam"
    SULPHURS = "Schwefeldioxid"
    SULFITES = "Sulfite"
    LUPIN = "Lupine"
    MOLLUSCS = "Weichtiere"
    SHELL_FRUITS = "Schalenfrüchte"

    BAVARIA = "Zertifizierte Qualität Bayern"
    MSC = "Marine Stewardship Council"
    DYESTUFF = "Farbstoffe"
    PRESERVATIVES = "Preservate"
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

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.name < other.value
        return NotImplemented

    @staticmethod
    def add_supertype_ingredients(ingredients: Set[Ingredient]) -> None:
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

    def to_json_obj(self):
        return {
            "name": self.name,
            "german_text": self.german_text,
        }


class Dish:
    name: str
    prices: Prices
    ingredients: Set[Ingredient]
    dish_type: str
    diet: Optional[Diet]

    def __init__(
        self,
        name: str,
        prices: Prices,
        ingredients: Set[Ingredient],
        dish_type: str,
        diet: Optional[Diet] = None,
    ):
        self.name = name
        self.prices = prices
        self.ingredients = ingredients
        self.dish_type = dish_type
        self.diet = diet

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
            "ingredients": sorted(map(str, self.ingredients)),
            "dish_type": self.dish_type,
            "diet": str(self.diet),
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
    def to_weeks(menus: Dict[datetime.date, Menu]) -> Dict[int, Week]:
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
