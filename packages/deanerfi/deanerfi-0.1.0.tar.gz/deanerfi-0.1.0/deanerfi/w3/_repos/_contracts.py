from typing import Protocol, Dict, Tuple

from eth_typing import ChecksumAddress

from deanerfi.utils.w3 import cs_addr
from deanerfi.w3 import ContractInfo
from deanerfi.utils.data import load_json, write_json, dataclass_from_dict
from deanerfi.utils.mongodb import MongoWrapper


class ContractRepo(Protocol):

    def get(self, chain_id: int, address: str) -> ContractInfo:
        pass

    def save(self, contract_info: ContractInfo) -> None:
        pass


class LocalContractRepo:
    """In memory Chain Repo that can be loaded/ saved to a json file
    Default file location is '<LOCAL_REPO_PATH>/token-repo.json'
    """

    def __init__(self, file_path: str = None, save_to_file: bool = True) -> None:
        self.file_path = file_path
        self.save_to_file = save_to_file
        self._contracts: Dict[Tuple[int, ChecksumAddress], ContractInfo] = {}
        if self.file_path:
            self._load()

    def _load(self) -> None:
        contract_dict = load_json(self.file_path)
        for contract in contract_dict:
            c_info = ContractInfo(**contract)
            self._contracts[(c_info.chain_id, c_info.address)] = c_info

    def get(self, chain_id: int, address: str) -> ContractInfo:
        return self._contracts.get((chain_id, cs_addr(address)))

    def save(self, contract_info: ContractInfo) -> None:
        self._contracts[(contract_info.chain_id, contract_info.address)] = contract_info
        if self.save_to_file and self.file_path:
            write_json(self.file_path, [contract.to_dict() for contract in self._contracts.values()])


class MongoDBContractRepo:
    _table: str = 'contracts'

    def __init__(self, mongo_wrapper: MongoWrapper = None) -> None:
        self._mongo = mongo_wrapper or MongoWrapper()

    def get(self, chain_id: int, address: str) -> ContractInfo:
        q = {'chain_id': chain_id, 'address': address}
        response = self._mongo.get(self._table, q)[0]
        return dataclass_from_dict(data_dict=response, d_class=ContractInfo)

    def save(self, contract_info: ContractInfo) -> None:
        self._mongo.upsert(
            self._table,
            contract_info.to_dict(),
            {'chain_id': contract_info.chain_id, 'address': contract_info.address}
        )
