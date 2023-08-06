from os import environ
from typing import Protocol

import requests

from deanerfi.w3 import ChainInfo
from deanerfi.utils.data import load_json, write_json
from deanerfi.utils.mongodb import MongoWrapper


class ChainRepo(Protocol):
    """Interface for a ChainRepo."""

    def get(self, chain_id: int) -> ChainInfo:
        """Get a ChainInfo by chain_id."""
        pass

    def save(self, chain_info: ChainInfo) -> None:
        """Save a ChainInfo to the repo."""
        pass


class LocalChainRepo:
    """In memory Chain Repo that can be loaded/ saved to a json file
    Default file location is '<LOCAL_REPO_PATH>/token-repo.json'
    """

    def __init__(self, file_path: str = None, save_to_file: bool = True) -> None:
        self.file_path = file_path
        self.save_to_file = save_to_file
        self._chains: dict[int, ChainInfo] = {}
        if self.file_path:
            self._load()

    def _load(self) -> None:
        """Load the repo from a json file."""
        chains_dict = load_json(self.file_path)
        for chain in chains_dict:
            if not chain.get('scanner_api_key'):
                chain['scanner_api_key'] = environ.get(f'{chain["symbol"]}_SCANNER_API_KEY')
            c_info = ChainInfo(**chain)
            self._chains[c_info.id] = c_info

    def get(self, chain_id: int) -> ChainInfo:
        """Get a ChainInfo by chain_id."""
        return self._chains.get(chain_id)

    def save(self, chain_info: ChainInfo) -> None:
        """Save a ChainInfo to the repo."""
        self._chains[chain_info.id] = chain_info
        if self.save_to_file and self.file_path:
            write_json(self.file_path, [chain.to_dict() for chain in self._chains.values()])


class MongoDBChainRepo:
    """Implements ChainRepo using MongoDB."""
    _table: str = 'chains'

    def __init__(self, mongo_wrapper: MongoWrapper = None) -> None:
        self._mongo = mongo_wrapper or MongoWrapper()

    def get(self, chain_id: int) -> ChainInfo:
        """Get a ChainInfo by chain_id."""
        response = self._mongo.get(self._table, {'id': chain_id})[0]
        _ = response.pop('_id')
        return ChainInfo(**response)

    def save(self, chain_info: ChainInfo) -> None:
        """Save a ChainInfo to the repo."""
        self._mongo.upsert(
            self._table,
            chain_info.to_dict(),
            {'id': chain_info.id}
        )


class HTTPDBChainRepo:
    """Implements ChainRepo using HTTP requests to an external API."""

    def __init__(self, api_url: str) -> None:
        self.api_url = api_url

    def get(self, chain_id: int) -> ChainInfo:
        response = requests.get(f'{self.api_url}/chains/{chain_id}')
        return ChainInfo(**response.json())

    def save(self, chain_info: ChainInfo) -> None:
        response = requests.post(f'{self.api_url}/chains/', json=chain_info.to_dict())
