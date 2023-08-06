from dataclasses import dataclass, field, asdict
from decimal import Decimal
from typing import List, Dict

from eth_typing import ChecksumAddress
from web3.constants import ADDRESS_ZERO

from deanerfi.utils.w3 import cs_addr
from deanerfi.w3 import ContractInfo


@dataclass(kw_only=True)
class DexInfo:
    name: str
    subtype: str
    chain_id: int
    id: str
    trading_fee: Decimal
    contracts: Dict[str, ContractInfo]
    pool_abi: List = None
    subgraph_url: str = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(kw_only=True)
class DexPoolInfo:
    address: ChecksumAddress
    tokens: List[ChecksumAddress]
    dex_id: str
    chain_id: int

    def __post_init__(self) -> None:
        self.tokens = [cs_addr(addr) for addr in self.tokens]
        self.tokens.sort()
        self.address = cs_addr(self.address)

    def __eq__(self, other: "DexPoolInfo") -> bool:
        return self.tokens == other.tokens

    def __str__(self) -> str:
        return f'{self.dex_id}: ' + ' - '.join([str(t) for t in self.tokens])

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self):
        return hash(self.address)

    def to_dict(self) -> dict:
        return asdict(self)

    def contains_any(self, tokens: List[ChecksumAddress]) -> bool:
        """Returns true if the pool contains any of the tokens in the list"""
        return any(token in self.tokens for token in tokens)

    def contains_all(self, tokens: List[ChecksumAddress]) -> bool:
        """Returns true if the pool contains all of the tokens in the list"""
        return all(token in self.tokens for token in tokens)

    @staticmethod
    def null_pool(tokens: List[ChecksumAddress]) -> 'DexPoolInfo':
        tokens.sort()
        return DexPoolInfo(
            address=ADDRESS_ZERO,
            tokens=tokens,
            dex_id='NULL',
            chain_id=-1
        )


@dataclass(kw_only=True)
class Swap:
    token_in: ChecksumAddress
    token_out: ChecksumAddress
    pool_address: ChecksumAddress
    amount_in: Decimal = field(default=Decimal('0'))
    amount_out: Decimal = field(default=Decimal('0'))

    def __eq__(self, other: 'Swap') -> bool:
        return self.pool_address == other.pool_address

    def __str__(self) -> str:
        return f'Pool: {self.pool_address}\n\t{self.amount_in} {self.token_in} -> {self.amount_out} {self.token_out}'

    def __repr__(self) -> str:
        return str(self)


@dataclass(kw_only=True)
class SwapRoute:
    route: List[Swap] = field(default_factory=list)

    class SwapRouteError(Exception):
        pass

    def add_swap(self, next_swap: Swap) -> None:
        if not self.route:
            self.route.append(next_swap)
            return
        _invalid_amount_in = next_swap.amount_in != self.route[-1].amount_out
        _invalid_token_in = next_swap.token_in != self.route[-1].token_out
        if _invalid_token_in or _invalid_amount_in:
            raise self.SwapRouteError(f'Swap Route Error: add_swap ')
        self.route.append(next_swap)

    @property
    def amount_in(self) -> Decimal:
        return self.route[0].amount_in

    @property
    def amount_out(self) -> Decimal:
        return self.route[-1].amount_out

    @property
    def token_in(self) -> ChecksumAddress:
        return self.route[0].token_in

    @property
    def token_out(self) -> ChecksumAddress:
        return self.route[-1].token_out

    def __str__(self) -> str:
        return f'Route: {self.amount_in} {self.token_in} -> {self.amount_out} {self.token_out}\n' + '\n'.join(
            [str(s) for s in self.route])

    def __repr__(self) -> str:
        return str(self)
