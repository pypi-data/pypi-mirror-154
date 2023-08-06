from typing import Protocol, List
from deanerfi.w3 import TokenInfo
from deanerfi.dex import DexPoolAPI


class Arbitrageur(Protocol):

    def run(self) -> None:
        pass


class PoolArbitrageur:

    def __init__(self, tokens: List[TokenInfo], pools: List[DexPoolAPI]) -> None:
        self.tokens = tokens
        self.tokens.sort()
        self.pools = pools

    def run(self) -> None:
        print(f'{self.tokens[0].name} - {self.tokens[0].address}')
        print(f'{self.tokens[1].name} - {self.tokens[1].address}')
        for pool in self.pools:
            print(pool.dex_id)
            pool_reserves = pool.get_reserves()
            num_t0 = self.tokens[0].from_wei(pool_reserves[self.tokens[0].address])
            num_t1 = self.tokens[1].from_wei(pool_reserves[self.tokens[1].address])

            print(f'  {self.tokens[0].symbol}: {int(num_t0)} ')
            print(f'  {self.tokens[1].symbol}: {int(num_t1)}')

            print(f'  {self.tokens[0].symbol}/{self.tokens[1].symbol}: {num_t0/num_t1}')
            print(f'  {self.tokens[1].symbol}/{self.tokens[0].symbol}: {num_t1 / num_t0}')





