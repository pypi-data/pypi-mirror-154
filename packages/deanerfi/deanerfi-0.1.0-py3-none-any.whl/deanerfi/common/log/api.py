from . import _config
from ._logger import DeanerfiLogger
from typing import Any


def get_logger() -> DeanerfiLogger:
    return _config.LOGGER


def set_logger(logger: DeanerfiLogger) -> None:
    _config.LOGGER = logger


def info(name: str, log_str: str, data: Any = None) -> None:
    _config.LOGGER.info(name=name, log_str=log_str, data=data)


def debug(name: str, log_str: str, data: Any = None) -> None:
    _config.LOGGER.debug(name=name, log_str=log_str, data=data)


def warn(name: str, log_str: str, data: Any = None) -> None:
    _config.LOGGER.warn(name=name, log_str=log_str, data=data)


def critical(name: str, log_str: str, data: Any = None) -> None:
    _config.LOGGER.critical(name=name, log_str=log_str, data=data)


def error(name: str, log_str: str, data: Any = None) -> None:
    _config.LOGGER.error(name=name, log_str=log_str, data=data)
