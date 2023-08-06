from typing import List, Set

from eth_typing import ChecksumAddress

from deanerfi.utils.data import load_json, write_json
from deanerfi.utils.mongodb import MongoWrapper
from ._adaptors import DexRepo
from ._dtypes import DexInfo, DexPoolInfo


class LocalDexRepo(DexRepo):

    def __init__(self, file_path: str = None, save_to_file: bool = True) -> None:
        self.file_path = file_path
        self.save_to_file = save_to_file
        self._configs: List[DexInfo] = list()
        self._pools: Set[DexPoolInfo] = set()
        if self.file_path:
            self._load()

    def get_configs(self, subtype: str = None, chain_id: int = None) -> List[DexInfo]:
        return_configs = self._configs
        if subtype:
            return_configs = [config for config in return_configs if config.subtype == subtype]
        if chain_id:
            return_configs = [config for config in return_configs if config.chain_id == chain_id]
        return return_configs

    def get_config(self, dex_id: str = None) -> DexInfo:
        return next(dex_config for dex_config in self._configs if dex_config.id == dex_id)

    def delete_dex(self, dex_id: str) -> None:
        self._configs = [dex_config for dex_config in self._configs if dex_config.id != dex_id]
        self._pools = [pool for pool in self._pools if pool.dex_id != dex_id]
        self._save_file()

    def token_pools(self, chain_id: int, tokens: List[ChecksumAddress]) -> List[DexPoolInfo]:
        return [pool for pool in self.chain_pools(chain_id=chain_id) if pool.contains_all(tokens)]

    def pools_w_tokens(self, chain_id: int, tokens: List[ChecksumAddress]) -> List[DexPoolInfo]:
        return [pool for pool in self.chain_pools(chain_id=chain_id) if pool.contains_any(tokens)]

    def dex_pools(self, dex_id: str) -> List[DexPoolInfo]:
        return [pool for pool in self._pools if pool.dex_id == dex_id]

    def get_pool_info(self, chain_id: int, address: ChecksumAddress) -> DexPoolInfo:
        return next(
            pool_info for pool_info in self._pools if
            pool_info.chain_id == chain_id and pool_info.address == address
        )

    def chain_pools(self, chain_id: int) -> List[DexPoolInfo]:
        return [pool for pool in self._pools if pool.chain_id == chain_id]

    def save_pools(self, pools: List[DexPoolInfo]) -> None:
        self._pools.update(set(pools))
        self._save_file()

    def save_configs(self, configs: List[DexInfo]) -> None:
        raise NotImplementedError

    def _load(self) -> None:
        dex_data = load_json(self.file_path)
        configs = dex_data.get('configs')
        pools = dex_data.get('pools')
        if configs:
            self._configs = [self._config_from_dict(conf) for conf in configs]
        if pools:
            self._pools = {self._pool_from_dict(pool) for pool in pools}

    def _save_file(self) -> None:
        if self.file_path and self.save_to_file:
            write_json(
                file_path=self.file_path,
                json_data={
                    'configs': [config.to_dict() for config in self._configs],
                    'pools': [pool.to_dict() for pool in self._pools]
                }
            )


class MongoDBDexRepo(DexRepo):

    def __init__(self, mongo_wrapper: MongoWrapper = None) -> None:
        self._mongo = mongo_wrapper or MongoWrapper()

    def get_configs(self, subtype: str = None, chain_id: int = None) -> List[DexInfo]:
        queue = {}
        if subtype:
            queue['subtype'] = subtype
        if chain_id:
            queue['chain_id'] = chain_id
        response = self._mongo.get('dex_configs', queue)
        return [self._config_from_dict(config) for config in response]

    def get_config(self, dex_id: str = None) -> DexInfo:
        response = self._mongo.get('dex_configs', {'id': dex_id})
        return self._config_from_dict(response[0])

    def delete_dex(self, dex_id: str) -> None:
        self._mongo.delete_one('dex_configs', {'id': dex_id})
        self._mongo.delete_many('dex_pools', {'dex_id': dex_id})

    def token_pools(self, chain_id: int, tokens: List[ChecksumAddress]) -> List[DexPoolInfo]:
        q_filter = {
            'chain_id': chain_id,
            'tokens': {
                '$all': tokens
            }
        }
        response = self._mongo.get('dex_pools', q_filter)
        return [self._pool_from_dict(pool) for pool in response]

    def pools_w_tokens(self, chain_id: int, tokens: List[ChecksumAddress]) -> List[DexPoolInfo]:
        q_filter = {
            'chain_id': chain_id,
            '$or': [
                {'tokens': {'$in': [token]}} for token in tokens
            ]
        }
        response = self._mongo.get('dex_pools', q_filter)
        return [self._pool_from_dict(pool) for pool in response]

    def dex_pools(self, dex_id: str) -> List[DexPoolInfo]:
        response = self._mongo.get('dex_pools', {'dex_id': dex_id})
        return [self._pool_from_dict(pool) for pool in response]

    def get_pool_info(self, chain_id: int, address: ChecksumAddress) -> DexPoolInfo:
        response = self._mongo.get(
            'dex_pools',
            {'chain_id': chain_id, 'address': address}
        )
        return self._pool_from_dict(response[0])

    def chain_pools(self, chain_id: int) -> List[DexPoolInfo]:
        response = self._mongo.get('dex_pools', {'chain_id': chain_id})
        return [self._pool_from_dict(pool) for pool in response]

    def save_pools(self, pools: List[DexPoolInfo]) -> None:
        for pool in pools:
            self._mongo.upsert(
                table='dex_pools',
                data=pool.to_dict(),
                id_dict={
                    'address': pool.address,
                    'dex_id': pool.dex_id,
                    'chain_id': pool.chain_id
                }
            )

    def save_configs(self, configs: List[DexInfo]) -> None:
        for dex_info in configs:
            self._mongo.upsert(
                table='dex_configs',
                data=dex_info.to_dict(),
                id_dict={
                    'dex_id': dex_info.id
                }
            )
