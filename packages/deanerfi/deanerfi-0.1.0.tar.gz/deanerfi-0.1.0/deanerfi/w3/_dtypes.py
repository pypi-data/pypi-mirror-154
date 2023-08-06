from dataclasses import dataclass, asdict
from decimal import Decimal
from typing import Union

from eth_typing import ChecksumAddress

from deanerfi.utils.w3 import cs_addr

TokenAmountType = Union[str, float, int, Decimal]


@dataclass(slots=True)
class ChainInfo:
    """Chain object stores the information needed to connect to an EVM blockchain with web3.py"""
    id: int
    name: str
    symbol: str
    rpc: str
    explorer: str = None
    scanner_api_key: str = None
    scanner_api_url: str = None
    inject_middleware: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class ContractInfo:
    """Contract object stores the information needed to connect to a web3.Contract"""
    chain_id: int
    address: ChecksumAddress
    abi: list = None
    name: str = None

    def __post_init__(self) -> None:
        self.address = cs_addr(self.address)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class TokenInfo:
    symbol: str
    name: str
    address: ChecksumAddress
    chain_id: int
    decimals: Decimal
    stable_coin: bool = False
    wl: bool = False

    def __post_init__(self) -> None:
        self.address = cs_addr(self.address)
        self.decimals = Decimal(self.decimals)

    @property
    def _base(self) -> Decimal:
        return Decimal('10') ** self.decimals

    def to_wei(self, amount: TokenAmountType) -> Decimal:
        """Returns the input amount of Ether in Wei format"""
        return Decimal(amount) * self._base

    def from_wei(self, amount: TokenAmountType) -> Decimal:
        """Returns the input amount of Wei in Ether format"""
        return Decimal(amount) / self._base

    def to_dict(self) -> dict:
        _dict = asdict(self)
        _dict['decimals'] = str(self.decimals)
        return _dict

    def __str__(self) -> str:
        return f'{self.name} ({self.symbol})'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: "TokenInfo") -> bool:
        return (
            self.address == other.address and
            self.chain_id == other.chain_id
        )

    def __lt__(self, other: "TokenInfo") -> bool:
        return self.address < other.address


@dataclass(slots=True)
class Wallet:
    address: ChecksumAddress
    name: str

    def __post_init__(self) -> None:
        self.address = cs_addr(self.address)


class ChainListError(Exception):
    """Raised when there is an error with the provided config"""
    pass


class ChainList:

    def __init__(self, chains: [ChainInfo] = None) -> None:
        self._chains: dict[int, ChainInfo] = {}
        if chains:
            self.add_chains(chains)

    def add_chain(self, chain: ChainInfo) -> None:
        self._chains[chain.id] = chain
        setattr(self, chain.symbol, chain)

    def add_chains(self, chains: [ChainInfo]) -> None:
        for chain in chains:
            self.add_chain(chain)

    def __getitem__(self, chain_id: int) -> ChainInfo:
        try:
            _chain = self._chains[chain_id]
        except KeyError as e:
            raise ChainListError(f'Error: ChainInfo for chain id {chain_id} not configured')
        return _chain
