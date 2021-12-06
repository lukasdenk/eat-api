# -*- coding: utf-8 -*-

# Postponed Evaluation of Annotations to allow using a class inside a class for annotations
from __future__ import annotations

import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set

from utils import json_util


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


class Location:
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


class Canteen(Enum):
    # Some of the canteens do not use the general Studentenwerk system and therefore do not have a url_id.
    def __init__(self, long_name: str, location: Location, url_id: int):
        self.long_name = long_name
        self.site = location
        self.url_id = url_id
        self.canteen_id = self.name.lower().replace("_", "-")

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

    @staticmethod
    def get_canteen_by_str(canteen_str: str) -> Canteen:
        return Canteen[canteen_str.upper().replace("-", "_")]

    def to_json_obj(self):
        return {
            "canteen_id": self.canteen_id,
            "name": self.name,
            "long_name": self.long_name,
            "site": self.site.to_json_obj(),
            "url_id": self.url_id,
        }


class Language(Enum):
    DE = auto()

    def to_json_obj(self):
        return {
            "name": self.name,
        }


class Label(Enum):
    def __init__(self, text: Dict[Language, str]):
        self.text = text

    GLUTEN = {Language.DE: "Gluten"}
    WHEAT = {Language.DE: "Weizen"}
    RYE = {Language.DE: "Roggen"}
    BARLEY = {Language.DE: "Gerste"}
    OAT = {Language.DE: "Hafer"}
    SPELT = {Language.DE: "Dinkel"}
    HYBRIDS = {Language.DE: "Hybridstämme"}
    SHELLFISH = {Language.DE: "Krebstiere"}
    CHICKEN_EGGS = {Language.DE: "Eier"}
    FISH = {Language.DE: "Fisch"}
    PEANUTS = {Language.DE: "Erdnüsse"}
    SOY = {Language.DE: "Soja"}
    MILK = {Language.DE: "Milch"}
    LACTOSE = {Language.DE: "Laktose"}
    ALMONDS = {Language.DE: "Mandeln"}
    HAZELNUTS = {Language.DE: "Haselnüsse"}
    WALNUTS = {Language.DE: "Walnüsse"}
    CASHEWS = {Language.DE: "Cashewnüsse"}
    PECAN = {Language.DE: "Pekanüsse"}
    PISTACHIOES = {Language.DE: "Pistazien"}
    MACADAMIA = {Language.DE: "Macadamianüsse"}
    CELERY = {Language.DE: "Sellerie"}
    MUSTARD = {Language.DE: "Senf"}
    SESAME = {Language.DE: "Sesam"}
    SULPHURS = {Language.DE: "Schwefeldioxid"}
    SULFITES = {Language.DE: "Sulfite"}
    LUPIN = {Language.DE: "Lupine"}
    MOLLUSCS = {Language.DE: "Weichtiere"}
    SHELL_FRUITS = {Language.DE: "Schalenfrüchte"}

    BAVARIA = {Language.DE: "Zertifizierte Qualität Bayern"}
    MSC = {Language.DE: "Marine Stewardship Council"}
    DYESTUFF = {Language.DE: "Farbstoffe"}
    PRESERVATIVES = {Language.DE: "Preservate"}
    ANTIOXIDANTS = {Language.DE: "Antioxidanten"}
    FLAVOR_ENHANCER = {Language.DE: "Geschmacksverstärker"}
    WAXED = {Language.DE: "Gewachst"}
    PHOSPATES = {Language.DE: "Phosphate"}
    SWEETENERS = {Language.DE: "Süßungsmittel"}
    PHENYLALANINE = {Language.DE: "Phenylaline"}
    COCOA_CONTAINING_GREASE = {Language.DE: "Kakaohaltiges Fett"}
    GELATIN = {Language.DE: "Gelatine"}
    ALCOHOL = {Language.DE: "Alkohol"}
    PORK = {Language.DE: "Schweinefleisch"}
    BEEF = {Language.DE: "Rinderfleisch"}
    VEAL = {Language.DE: "Kalbsfleisch"}
    WILD_MEAT = {Language.DE: "Wildfleisch"}
    LAMB = {Language.DE: "Lammfleisch"}
    GARLIC = {Language.DE: "Knoblauch"}
    POULTRY = {Language.DE: "Geflügel"}
    CEREAL = {Language.DE: "Getreide"}
    MEAT = {Language.DE: "Fleisch"}
    VEGAN = {Language.DE: "Vegan"}
    VEGETARIAN = {Language.DE: "Vegetarisch"}

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.name < other.value
        return NotImplemented

    @staticmethod
    def add_supertype_labels(labels: Set[Label]) -> None:
        # insert supertypes
        if labels & {
            Label.ALMONDS,
            Label.HAZELNUTS,
            Label.MACADAMIA,
            Label.CASHEWS,
            Label.PECAN,
            Label.PISTACHIOES,
            Label.SESAME,
            Label.WALNUTS,
        }:
            labels |= {Label.SHELL_FRUITS}
        if labels & {
            Label.BARLEY,
            Label.OAT,
            Label.RYE,
            Label.SPELT,
            Label.WHEAT,
        }:
            labels |= {Label.CEREAL}
        if labels & {Label.VEGAN}:
            labels |= {Label.VEGETARIAN}

        if labels & {
            Label.PORK,
            Label.BEEF,
            Label.VEAL,
        }:
            labels |= {Label.MEAT}

    def to_json_obj(self):
        return {
            "name": self.name,
            "text": json_util.dict_to_json_dict(self.text),
        }


class Dish:
    name: str
    prices: Prices
    labels: Set[Label]
    dish_type: str

    def __init__(
        self,
        name: str,
        prices: Prices,
        labels: Set[Label],
        dish_type: str,
    ):
        self.name = name
        self.prices = prices
        self.labels = labels
        self.dish_type = dish_type

    def __repr__(self):
        return f"{self.name} {str(sorted(self.labels))}: {str(self.prices)}"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return (
                self.name == other.name
                and self.prices == other.prices
                and self.labels == other.labels
                and self.dish_type == other.dish_type
            )
        return False

    def to_json_obj(self):
        return {
            "name": self.name,
            "prices": self.prices.to_json_obj(),
            "labels": sorted(map(str, self.labels)),
            "dish_type": self.dish_type,
        }

    def __hash__(self) -> int:
        # http://stackoverflow.com/questions/4005318/how-to-implement-a-good-hash-function-in-python
        return (hash(self.name) << 1) ^ hash(self.prices) ^ hash(frozenset(self.labels)) ^ hash(self.dish_type)


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
