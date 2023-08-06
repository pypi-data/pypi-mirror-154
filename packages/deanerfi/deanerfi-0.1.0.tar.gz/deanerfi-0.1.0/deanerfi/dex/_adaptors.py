from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Callable, Type, Dict

from eth_typing import ChecksumAddress
from web3.contract import Contract

from deanerfi.utils.data import dataclass_from_dict
from ._dtypes import DexInfo, DexPoolInfo
from deanerfi.w3 import ContractInfo

ContractLoader = Callable[[int, ChecksumAddress, list], Contract]


class DexAPI(ABC):
    """Interface for interacting with a DEX contract."""

    def __init__(self, name: str, subtype: str, chain_id: int, trading_fee: Decimal, dex_id: str,
                 addresses: Dict[str, ChecksumAddress], contract_loader: ContractLoader, **kwargs) -> None:
        self.name = name
        self.subtype = subtype
        self.chain_id = chain_id
        self.trading_fee = trading_fee
        self.id = dex_id
        self.chain_id = chain_id
        self.addresses = addresses
        self._contract_loader = contract_loader

    @abstractmethod
    def tradable(self, token0: ChecksumAddress, token1: ChecksumAddress) -> bool:
        """Check if a pair of tokens is tradable."""
        raise NotImplementedError

    @abstractmethod
    def quote(self, token0: ChecksumAddress, token1: ChecksumAddress, amount: int) -> Decimal:
        """Get the quote price for token0 in relation to token1."""
        raise NotImplementedError

    @abstractmethod
    def get_pool_api(self, pool_info: DexPoolInfo) -> 'DexPoolAPI':
        """Build a DEXPoolAPI from a DexPoolInfo object."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def build(config: DexInfo, contract_loader: ContractLoader, **kwargs) -> 'DexAPI':
        """Build a DEX contract from a DexInfo object."""
        raise NotImplementedError


class DexPoolAPI(ABC):
    """Interface for interacting with a DEX pool contract."""

    def __init__(self, dex_id: str, address: ChecksumAddress, chain_id: int,
                 tokens: List[ChecksumAddress], pool_contract: Contract) -> None:
        self.dex_id = dex_id
        self.chain_id = chain_id
        self.address = address
        self.tokens = tokens
        self._contract = pool_contract

    @abstractmethod
    def get_reserves(self) -> Dict[ChecksumAddress, Decimal]:
        """Get the current reserve of each token in the pool."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def build(config: DexPoolInfo, pool_abi: list, contract_loader: ContractLoader, **kwargs) -> 'DexPoolAPI':
        """Build a DexPoolAPI from a DexPoolInfo."""
        raise NotImplementedError

    def __eq__(self, other: "DexPoolAPI") -> bool:
        return self.tokens == other.tokens

    def __str__(self) -> str:
        return f'{self.dex_id}: ' + ' - '.join([str(t) for t in self.tokens])

    def __repr__(self) -> str:
        return str(self)


class DexRepo(ABC):
    """Interface for interacting with a DEX repository."""

    @staticmethod
    def _pool_from_dict(pool_dict: dict) -> DexPoolInfo:
        return dataclass_from_dict(
            pool_dict,
            DexPoolInfo
        )

    @staticmethod
    def _config_from_dict(dex_dict: dict) -> DexInfo:
        """Convert a DEX config dict to a DEXInfo object."""
        for contract_name, contract_dict in dex_dict['contracts'].items():
            dex_dict['contracts'][contract_name] = ContractInfo(**contract_dict)
        return dataclass_from_dict(
            dex_dict,
            DexInfo
        )

    @abstractmethod
    def get_configs(self, subtype: str = None, chain_id: int = None) -> List[DexInfo]:
        """Get DexInfo objects for all DEXes of a given subtype on a given chain."""
        raise NotImplementedError

    @abstractmethod
    def get_config(self, dex_id: str = None) -> DexInfo:
        """Get DexInfo object for a given DEX."""
        raise NotImplementedError

    @abstractmethod
    def delete_dex(self, dex_id: str) -> None:
        """Delete a DEX from the repository."""
        raise NotImplementedError

    @abstractmethod
    def token_pools(self, chain_id: int, tokens: List[ChecksumAddress]) -> List[DexPoolInfo]:
        """Returns the Dex's pools containing only the supplied tokens"""
        raise NotImplementedError

    @abstractmethod
    def pools_w_tokens(self, chain_id: int, tokens: List[ChecksumAddress]) -> List[DexPoolInfo]:
        """Returns all pools that contain any of the supplied tokens"""
        raise NotImplementedError

    @abstractmethod
    def dex_pools(self, dex_id: str) -> List[DexPoolInfo]:
        """Gets all pools for the given dex"""
        raise NotImplementedError

    @abstractmethod
    def get_pool_info(self, chain_id: int, address: ChecksumAddress) -> DexPoolInfo:
        """Gets all pools for the given dex"""
        raise NotImplementedError

    @abstractmethod
    def chain_pools(self, chain_id: int) -> List[DexPoolInfo]:
        """Gets all pools for the given dex"""
        raise NotImplementedError

    @abstractmethod
    def save_pools(self, pools: List[DexPoolInfo]) -> None:
        """Saves the pools to persistent storage"""
        raise NotImplementedError

    @abstractmethod
    def save_configs(self, configs: List[DexInfo]) -> None:
        """Saves the DexInfo to persistent storage"""
        raise NotImplementedError


class DexDataLoader(ABC):
    """Interface for loading Dex data into the DexRepo. Most data is loaded from The Graph."""

    @abstractmethod
    def load_data(self, dex_info: DexInfo, repo: DexRepo) -> None:
        raise NotImplementedError


@dataclass
class DexPackage:
    """Class that groups the dex config (DexInfo), api (DexAPI), and data loader (DexDataLoader) into a package that can
    keep track of the components required to fully integrate with a dex.
    """
    subtype: str
    dex_api: Type[DexAPI]
    pool_api: Type[DexPoolAPI]
    data_loader: Type[DexDataLoader] = field(default=None)
