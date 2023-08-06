import importlib.resources as pkg_resources
from typing import Type, Union

from deanerfi import data
import json
from dataclasses import dataclass


def _load_pkg_data(file: str):
    return json.loads(
        pkg_resources.read_text(data, file)
    )


def erc20_abi() -> list:
    return _load_pkg_data('erc20-abi.json')


def load_json(file_path: str):
    with open(file_path) as f:
        json_data = json.load(f)
    return json_data


def write_json(file_path: str, json_data: Union[list, dict]) -> None:
    with open(file_path, 'w') as f:
        json.dump(json_data, f)


def dataclass_from_dict(data_dict: dict, d_class: Type[dataclass]):
    return d_class(**{
        k: data_dict.get(k) for k, f in d_class.__dataclass_fields__.items() if f.init
    })
