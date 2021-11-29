import json

from lxml import html  # nosec: https://github.com/TUM-Dev/eat-api/issues/19


def load_html(path: str) -> html.Element:
    with open(path, encoding="utf-8") as f:
        html_element = html.fromstring(f.read())
    # suppress flake8 warning about "unnecessary variable assignment before return statement".
    # reason: file closing could otherwise have side-effects
    return html_element  # noqa: R504


def load_ordered_json(path: str) -> object:  # type: ignore
    with open(path, encoding="utf-8") as f:
        json_obj = json.load(f)
    # suppress flake8 warning about "unnecessary variable assignment before return statement".
    # reason: file closing could otherwise have side-effects
    return order_json_objects(json_obj)  # noqa: R504


def load_txt(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # suppress flake8 warning about "unnecessary variable assignment before return statement".
    # reason: file closing could otherwise have side-effects
    return text  # noqa: R504


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
