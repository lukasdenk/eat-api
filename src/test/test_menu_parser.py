# -*- coding: utf-8 -*-
import datetime
import json
import os
import tempfile
import unittest
from datetime import date
from typing import List

from lxml import html  # nosec: https://github.com/TUM-Dev/eat-api/issues/19

from src import main
from src.entities import Week
from src.menu_parser import (
    FMIBistroMenuParser,
    IPPBistroMenuParser,
    MedizinerMensaMenuParser,
    MenuParser,
    StudentenwerkMenuParser,
)
from src.test import test_util


class MenuParserTest(unittest.TestCase):
    def test_get_date(self):
        self.assertEqual(date(2017, 10, 30), MenuParser.get_date(2017, 44, 1))
        self.assertEqual(date(2018, 1, 1), MenuParser.get_date(2018, 1, 1))
        self.assertEqual(date(2019, 1, 7), MenuParser.get_date(2019, 2, 1))


class StudentenwerkMenuParserTest(unittest.TestCase):
    studentenwerk_menu_parser = StudentenwerkMenuParser()

    base_path_location = "src/test/assets/studentenwerk/{location}"

    test_dates = [
        date(2021, 9, 13),
        date(2021, 9, 14),
        date(2021, 9, 15),
        date(2021, 9, 16),
        date(2021, 9, 17),
        date(2021, 9, 20),
        date(2021, 9, 21),
        date(2021, 9, 22),
        date(2021, 9, 23),
        date(2021, 9, 24),
    ]

    test_dates_nov = []

    start_date = date(2021, 11, 1)
    end_date = date(2021, 12, 1)

    # all work days in november
    while start_date < end_date:
        # 5 means Saturday and so on
        if start_date.weekday() not in {5, 6}:
            test_dates_nov += [start_date]
        start_date += datetime.timedelta(days=1)

    def test_studentenwerk(self) -> None:
        locations = ["mensa-garching", "mensa-arcisstr", "stubistro-großhadern"]
        for location in locations:
            self.__test_studentenwerk_location(location)

    def test_get_dates(self) -> None:
        tree = test_util.load_html(
            f"{self.base_path_location.format(location='mensa-garching')}/for-generation/overview.html",
        )
        dates: List[date] = self.studentenwerk_menu_parser.get_available_dates_for_html(tree)
        self.assertEqual(self.test_dates_nov, dates)

    def __test_studentenwerk_location(self, location: str) -> None:
        menus = self.__get_menus(location)
        weeks = Week.to_weeks(menus)

        # create temp dir for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # store output in the tempdir
            main.jsonify(weeks, temp_dir, location, True)
            generated = test_util.load_json(os.path.join(temp_dir, "combined", "combined.json"))
            reference = test_util.load_json(
                f"{self.base_path_location.format(location=location)}/reference/combined.json",
            )
            self.assertEqual(generated, reference)

    def __get_menus(self, location):
        menus = {}
        for date_ in self.test_dates:
            # parse the menu
            tree: html.Element = test_util.load_html(
                f"{self.base_path_location.format(location=location)}/for-generation/{date_}.html",
            )
            studentenwerk_menu_parser = StudentenwerkMenuParser()
            menus[date_] = studentenwerk_menu_parser.get_menu(tree, location, date_)
        return menus

    def test_should_return_weeks_when_converting_menu_to_week_objects(self):
        menus = self.__get_menus("mensa-garching")
        weeks_actual = Week.to_weeks(menus)
        length_weeks_actual = len(weeks_actual)

        self.assertEqual(2, length_weeks_actual)
        for calendar_week in weeks_actual:
            week = weeks_actual[calendar_week]
            week_length = len(week.days)
            self.assertEqual(5, week_length)

    def test_should_convert_week_to_json(self):
        calendar_weeks = [37, 38]
        menus = self.__get_menus("mensa-garching")
        weeks = Week.to_weeks(menus)
        for calendar_week in calendar_weeks:
            reference_week = test_util.load_json(
                f"{self.base_path_location.format(location='mensa-garching')}/reference/week_{calendar_week}.json",
            )
            generated_week = weeks[calendar_week].to_json_obj()
            self.assertEqual(test_util.order_json_objects(generated_week), test_util.order_json_objects(reference_week))


class FMIBistroParserTest(unittest.TestCase):
    bistro_parser = FMIBistroMenuParser()

    def test_fmi_bistro(self):
        for_generation_path = "src/test/assets/fmi/for-generation/calendar_week_2021_{calendar_week}.txt"
        menus = {}
        for calendar_week in range(44, 46):
            text = test_util.load_txt(for_generation_path.format(calendar_week=calendar_week))
            menus.update(self.bistro_parser.get_menus(text, 2021, calendar_week))
        weeks = Week.to_weeks(menus)

        # create temp dir for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # store output in the tempdir
            main.jsonify(weeks, temp_dir, "fmi-bistro", True)
            generated = test_util.load_json(os.path.join(temp_dir, "combined", "combined.json"))
            reference = test_util.load_json("src/test/assets/fmi/reference/combined.json")

            self.assertEqual(test_util.order_json_objects(generated), test_util.order_json_objects(reference))


class IPPBistroParserTest(unittest.TestCase):
    ipp_parser = IPPBistroMenuParser()

    with open("src/test/assets/ipp/in/menu_kw_47_2017.txt", "r", encoding="utf-8") as menu_kw_47_2017:
        menu_kw_47_2017_txt = menu_kw_47_2017.read()
    menu_kw_47_2017_year = 2017
    menu_kw_47_2017_week_number = 47

    with open("src/test/assets/ipp/in/menu_kw_48_2017.txt", "r", encoding="utf-8") as menu_kw_48_2017:
        menu_kw_48_2017_txt = menu_kw_48_2017.read()
    menu_kw_48_2017_year = 2017
    menu_kw_48_2017_week_number = 48

    def test_ipp_bistro_kw_47_2017(self):
        # parse the menu
        menus = self.ipp_parser.get_menus(
            self.menu_kw_47_2017_txt,
            self.menu_kw_47_2017_year,
            self.menu_kw_47_2017_week_number,
        )
        weeks = Week.to_weeks(menus)

        # create temp dir for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # store output in the tempdir
            main.jsonify(weeks, temp_dir, "ipp-bistro", True)
            # open the generated file
            with open(os.path.join(temp_dir, "combined", "combined.json"), "r", encoding="utf-8") as generated:
                # open the reference file
                with open("src/test/assets/ipp/out/menu_kw_47_2017.json", "r", encoding="utf-8") as reference:
                    self.assertEqual(json.load(generated), json.load(reference))

    def test_ipp_bistro_kw_48_2017(self):
        # parse the menu
        menus = self.ipp_parser.get_menus(
            self.menu_kw_48_2017_txt,
            self.menu_kw_48_2017_year,
            self.menu_kw_48_2017_week_number,
        )
        weeks = Week.to_weeks(menus)

        # create temp dir for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # store output in the tempdir
            main.jsonify(weeks, temp_dir, "ipp-bistro", True)
            # open the generated file
            with open(os.path.join(temp_dir, "combined", "combined.json"), "r", encoding="utf-8") as generated:
                # open the reference file
                with open("src/test/assets/ipp/out/menu_kw_48_2017.json", "r", encoding="utf-8") as reference:
                    self.assertEqual(json.load(generated), json.load(reference))

    # Test Cases with holidays

    # Two holidays (Mon & Tue)
    with open("src/test/assets/ipp/in/menu_kw_18_2018.txt", "r", encoding="utf-8") as menu_kw_18_2018:
        menu_kw_18_2018_txt = menu_kw_18_2018.read()
    menu_kw_18_2018_year = 2018
    menu_kw_18_2018_week_number = 18

    def test_ipp_bistro_kw_18_2018_closed_monday_tuesday(self):
        # parse the menu
        menus = self.ipp_parser.get_menus(
            self.menu_kw_18_2018_txt,
            self.menu_kw_18_2018_year,
            self.menu_kw_18_2018_week_number,
        )
        weeks = Week.to_weeks(menus)

        # create temp dir for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # store output in the tempdir
            main.jsonify(weeks, temp_dir, "ipp-bistro", True)
            # open the generated file
            with open(os.path.join(temp_dir, "combined", "combined.json"), "r", encoding="utf-8") as generated:
                # open the reference file
                with open("src/test/assets/ipp/out/menu_kw_18_2018.json", "r", encoding="utf-8") as reference:
                    self.assertEqual(json.load(generated), json.load(reference))

    # One holiday (Thu)
    with open("src/test/assets/ipp/in/menu_kw_19_2018.txt", "r", encoding="utf-8") as menu_kw_19_2018:
        menu_kw_19_2018_txt = menu_kw_19_2018.read()
    menu_kw_19_2018_year = 2018
    menu_kw_19_2018_week_number = 19

    def test_ipp_bistro_kw_19_2018_closed_thursday(self):
        # parse the menu
        menus = self.ipp_parser.get_menus(
            self.menu_kw_19_2018_txt,
            self.menu_kw_19_2018_year,
            self.menu_kw_19_2018_week_number,
        )
        weeks = Week.to_weeks(menus)

        # create temp dir for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # store output in the tempdir
            main.jsonify(weeks, temp_dir, "ipp-bistro", True)
            # open the generated file
            with open(os.path.join(temp_dir, "combined", "combined.json"), "r", encoding="utf-8") as generated:
                # open the reference file
                with open("src/test/assets/ipp/out/menu_kw_19_2018.json", "r", encoding="utf-8") as reference:
                    self.assertEqual(json.load(generated), json.load(reference))

    # "Überraschungsmenü" and "Geschlossen" in first line of table
    with open("src/test/assets/ipp/in/menu_kw_22_2019.txt", "r", encoding="utf-8") as menu_kw_22_2019:
        menu_kw_22_2019_txt = menu_kw_22_2019.read()
    menu_kw_22_2019_year = 2019
    menu_kw_22_2019_week_number = 22

    def test_ipp_bistro_kw_22_2019_closed_thursday(self):
        # parse the menu
        menus = self.ipp_parser.get_menus(
            self.menu_kw_22_2019_txt,
            self.menu_kw_22_2019_year,
            self.menu_kw_22_2019_week_number,
        )
        weeks = Week.to_weeks(menus)

        # create temp dir for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # store output in the tempdir
            main.jsonify(weeks, temp_dir, "ipp-bistro", True)
            # open the generated file
            with open(os.path.join(temp_dir, "combined", "combined.json"), "r", encoding="utf-8") as generated:
                # open the reference file
                with open("src/test/assets/ipp/out/menu_kw_22_2019.json", "r", encoding="utf-8") as reference:
                    self.assertEqual(json.load(generated), json.load(reference))

    """
    # just for generating reference json files
    def test_gen_file(self):
        # parse the menu
        menus = self.ipp_parser.get_menus(
            self.menu_kw_22_2019_txt,
            self.menu_kw_22_2019_year,
            self.menu_kw_22_2019_week_number,
        )
        weeks = Week.to_weeks(menus)
        main.jsonify(weeks, "/tmp/eat-api_test_output", "ipp-bistro", True)
    """


class MedizinerMensaParserTest(unittest.TestCase):
    mediziner_mensa_parser = MedizinerMensaMenuParser()

    with open("src/test/assets/mediziner-mensa/in/menu_kw_44_2018.txt", "r", encoding="utf-8") as menu_kw_44_2018:
        menu_kw_44_2018_txt = menu_kw_44_2018.read()
    menu_kw_44_2018_year = 2018
    menu_kw_44_2018_week_number = 44

    with open("src/test/assets/mediziner-mensa/in/menu_kw_47_2018.txt", "r", encoding="utf-8") as menu_kw_47_2018:
        menu_kw_47_2018_txt = menu_kw_47_2018.read()
    menu_kw_47_2018_year = 2018
    menu_kw_47_2018_week_number = 47

    def test_mediziner_mensa_kw_44_2018(self):
        # parse the menu
        menus = self.mediziner_mensa_parser.get_menus(
            self.menu_kw_44_2018_txt,
            self.menu_kw_44_2018_year,
            self.menu_kw_44_2018_week_number,
        )
        weeks = Week.to_weeks(menus)

        # create temp dir for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # store output in the tempdir
            main.jsonify(weeks, temp_dir, "mediziner-mensa", True)
            # open the generated file
            with open(os.path.join(temp_dir, "combined", "combined.json"), "r", encoding="utf-8") as generated:
                # open the reference file
                with open(
                    "src/test/assets/mediziner-mensa/out/menu_kw_44_2018.json",
                    "r",
                    encoding="utf-8",
                ) as reference:
                    self.assertEqual(json.load(generated), json.load(reference))

    def test_mediziner_mensa_kw_47_2018(self):
        # parse the menu
        menus = self.mediziner_mensa_parser.get_menus(
            self.menu_kw_47_2018_txt,
            self.menu_kw_47_2018_year,
            self.menu_kw_47_2018_week_number,
        )
        weeks = Week.to_weeks(menus)

        # create temp dir for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # store output in the tempdir
            main.jsonify(weeks, temp_dir, "mediziner-mensa", True)
            # open the generated file
            with open(os.path.join(temp_dir, "combined", "combined.json"), "r", encoding="utf-8") as generated:
                # open the reference file
                with open(
                    "src/test/assets/mediziner-mensa/out/menu_kw_47_2018.json",
                    "r",
                    encoding="utf-8",
                ) as reference:
                    self.assertEqual(json.load(generated), json.load(reference))

    # """
    # just for generating reference json files
    def test_gen_file(self):
        # parse the menu
        menus = self.mediziner_mensa_parser.get_menus(
            self.menu_kw_47_2018_txt,
            self.menu_kw_47_2018_year,
            self.menu_kw_47_2018_week_number,
        )
        weeks = Week.to_weeks(menus)
        main.jsonify(weeks, "/tmp/eat-api_test_output", "mediziner-mensa", True)

    # """
