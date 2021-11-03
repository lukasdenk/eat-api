import json

# somehow, pylint and mypy do not recognize the "Union" class
# pylint:disable=no-name-in-module
from types import Union  # type: ignore #(for mypy)

from lxml import html  # nosec: https://github.com/TUM-Dev/eat-api/issues/19

# pylint:enable=no-name-in-module


def load_html(path: str) -> html.Element:
    with open(path, encoding="utf-8") as f:
        html_element = html.fromstring(f.read())
    # suppress flake8 warning about "unnecessary variable assignment before return statement".
    # reason: file closing could otherwise have side-effects
    return html_element  # noqa: R504


def load_json(path: Union[bytes, str]) -> object:
    with open(path, encoding="utf-8") as f:
        json_obj = json.load(f)
    # suppress flake8 warning about "unnecessary variable assignment before return statement".
    # reason: file closing could otherwise have side-effects
    return json_obj  # noqa: R504


def order_json_objects(obj):
    """
    Recusively orders all elemts in a Json object.
    Source:
    https://stackoverflow.com/questions/25851183/how-to-compare-two-json-objects-with-the-same-elements-in-a-different-order-equa
    """
    if isinstance(obj, dict):
        return sorted((k, order_json_objects(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(order_json_objects(x) for x in obj)
    return obj
