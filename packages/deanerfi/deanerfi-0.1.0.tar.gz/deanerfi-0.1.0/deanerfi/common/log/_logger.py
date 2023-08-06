import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from time import gmtime
from enum import Enum

from deanerfi.utils.mongodb import MongoWrapper


class LogLevel(Enum):
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARN = logging.WARNING
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR


class DeanerfiLogger(ABC):

    @abstractmethod
    def log(self, name: str, lvl: LogLevel, log_str: str, data: Any = None) -> None:
        raise NotImplementedError

    def info(self, name: str, log_str: str, data: Any = None) -> None:
        self.log(name, LogLevel.INFO, log_str, data=data)

    def debug(self, name: str, log_str: str, data: Any = None) -> None:
        self.log(name, LogLevel.DEBUG, log_str, data=data)

    def warn(self, name: str, log_str: str, data: Any = None) -> None:
        self.log(name, LogLevel.WARN, log_str, data=data)

    def critical(self, name: str, log_str: str, data: Any = None) -> None:
        self.log(name, LogLevel.CRITICAL, log_str, data=data)

    def error(self, name: str, log_str: str, data: Any = None) -> None:
        self.log(name, LogLevel.ERROR, log_str, data=data)


class LocalLogger(DeanerfiLogger):

    def __init__(self) -> None:
        logging.Formatter.converter = gmtime
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s : %(name)s %(message)s')

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

    def log(self, name: str, lvl: LogLevel, log_str: str, data: Any = None) -> None:
        _logger = self.get_logger(name)
        _logger.log(level=lvl.value, msg=log_str)
        if data:
            _logger.log(level=lvl.value, msg=data)


class MongoDBLogger(DeanerfiLogger):
    _table: str = 'logs'

    def __init__(self, mongo_wrapper: MongoWrapper = None) -> None:
        self._mongo = mongo_wrapper or MongoWrapper()

    def log(self, name: str, lvl: LogLevel, log_str: str, data: Any = None) -> None:
        self._mongo.put(
            self._table,
            {
                'datetime': str(datetime.utcnow()),
                'name': name,
                'log_level': lvl.value,
                'msg': log_str,
                'data': data
            }
        )
