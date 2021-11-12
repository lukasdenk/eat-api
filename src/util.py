# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Callable, List, TypeVar

date_pattern = "%d.%m.%Y"
cli_date_format = "dd.mm.yyyy"


def parse_date(date_str):
    return datetime.strptime(date_str, date_pattern).date()


def make_duplicates_unique(names_with_duplicates):
    counts = [1] * len(names_with_duplicates)
    checked_names = []
    for i, name in enumerate(names_with_duplicates):
        if name in checked_names:
            counts[i] += 1
        checked_names.append(name)

    names_without_duplicates = names_with_duplicates
    for i, count in enumerate(counts):
        if count > 1:
            names_without_duplicates[i] += f" ({count})"

    return names_without_duplicates


T = TypeVar("T")


def get_index_first_match(list_: List[T], predicate: Callable[[T], bool]):
    i = 0
    for i in range(len(list_)):
        if predicate(list_[i]):
            return i
        i += 1
    return -1
