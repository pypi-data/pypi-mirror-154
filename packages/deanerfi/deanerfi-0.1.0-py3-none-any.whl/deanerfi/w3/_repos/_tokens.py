from typing import Protocol, Optional, List

from deanerfi.w3._dtypes import TokenInfo
from deanerfi.utils.data import load_json, _load_pkg_data, write_json, dataclass_from_dict
from deanerfi.utils.mongodb import MongoWrapper

ERC20_ABI = _load_pkg_data('erc20-abi.json')


class TokenRepo(Protocol):

    def get_chain(self, chain_id: int) -> [TokenInfo]:
        pass

    def get_token(self, chain_id: int, address: str) -> TokenInfo:
        pass

    def get_wl_token(self, chain_id: int) -> List[TokenInfo]:
        pass

    def save(self, token_info: TokenInfo) -> None:
        pass

    def whitelist(self, address: str, chain_id: int, wl: bool = True) -> None:
        pass

    def stable_coin(self, address: str, chain_id: int, stable_coin: bool = True) -> None:
        pass


class LocalTokenRepo:

    def __init__(self, file_path: str = None, save_to_file: bool = True) -> None:
        self.file_path = file_path
        self.save_to_file = save_to_file
        self._tokens: dict[int, dict[str, TokenInfo]] = {}
        if self.file_path:
            self._load()

    def _load(self) -> None:
        for token in load_json(self.file_path):
            self._save_token(TokenInfo(**token))

    def get_chain(self, chain_id: int) -> [TokenInfo]:
        chain_tokens = self._tokens.get(chain_id)
        if not chain_tokens:
            return []
        return list(chain_tokens.values())

    def get_token(self, chain_id: int, address: str) -> Optional[TokenInfo]:
        return self._tokens.get(chain_id, {}).get(address)

    def get_wl_token(self, chain_id: int) -> List[TokenInfo]:
        return [token for token in self.get_chain(chain_id=chain_id) if token.wl]

    def _save_token(self, token_info: TokenInfo) -> None:
        if token_info.chain_id not in self._tokens:
            self._tokens[token_info.chain_id] = {}
        self._tokens[token_info.chain_id][token_info.address] = token_info

    def _save_file(self) -> None:
        if self.file_path and self.save_to_file:
            tokens = []
            for chain_id, token_dict in self._tokens.items():
                tokens += [token.to_dict() for token in token_dict.values()]
            write_json(
                self.file_path,
                tokens
            )

    def save(self, token_info: TokenInfo) -> None:
        self._save_token(token_info)
        self._save_file()

    def whitelist(self, address: str, chain_id: int, wl: bool = True) -> None:
        token = self.get_token(chain_id=chain_id, address=address)
        if token:
            token.wl = wl
            self._save_file()

    def stable_coin(self, address: str, chain_id: int, stable_coin: bool = True) -> None:
        token = self.get_token(chain_id=chain_id, address=address)
        if token:
            token.stable_coin = stable_coin
            self._save_file()


class MongoDBTokenRepo:
    _table: str = 'tokens'

    def __init__(self) -> None:
        self._mongo = MongoWrapper()

    def get_chain(self, chain_id: int) -> [TokenInfo]:
        response = self._mongo.get(self._table, {'chain_id': chain_id})
        _tokens = []
        for t in response:
            _tokens.append(dataclass_from_dict(
                t,
                TokenInfo
            ))
        return _tokens

    def get_token(self, chain_id: int, address: str) -> TokenInfo:
        response = self._mongo.get_one(self._table, {'chain_id': chain_id, 'address': address})
        if response:
            return dataclass_from_dict(
                response,
                TokenInfo
            )

    def get_wl_token(self, chain_id: int) -> List[TokenInfo]:
        response = self._mongo.get(self._table, {'chain_id': chain_id, 'wl': True})
        _tokens = []
        for t in response:
            _ = t.pop('_id')
            _tokens.append(TokenInfo(**t))
        return _tokens

    def save(self, token_info: TokenInfo) -> None:
        self._mongo.upsert(
            table=self._table,
            data=token_info.to_dict(),
            id_dict={'chain_id': token_info.chain_id, 'address': token_info.address}
        )

    def whitelist(self, address: str, chain_id: int, wl: bool = True) -> None:
        token = self.get_token(chain_id=chain_id, address=address)
        if token:
            token.wl = wl
            self.save(token)

    def stable_coin(self, address: str, chain_id: int, stable_coin: bool = True) -> None:
        token = self.get_token(chain_id=chain_id, address=address)
        if token:
            token.stable_coin = stable_coin
            self.save(token)
