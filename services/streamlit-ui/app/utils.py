from collections import abc
from typing import Any, Dict


def get_nested_value(d: Dict, key: str, sep=".") -> Any:
    keys = key.split(sep)
    current = d
    for key in keys:
        if isinstance(current, abc.Mapping) and key in current:
            current = current[key]
        else:
            raise KeyError(f"Key '{key}' not found in the dictionary.")
    return current


def set_nested_value(d: Dict, key: str, value: Any, sep=".") -> None:
    keys = key.split(sep)
    current = d
    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value