from decimal import Decimal
from typing import List, Tuple, Dict

from eth_typing import ChecksumAddress
from web3.contract import Contract
from deanerfi.common.log import api as log

from deanerfi.utils import graphql
from deanerfi.utils.data import _load_pkg_data
from ._adaptors import DexRepo, DexPoolAPI, DexPackage, DexAPI, ContractLoader, DexDataLoader
from ._dtypes import DexInfo, DexPoolInfo

UNISWAP_V2_DEFAULTS = _load_pkg_data('uniswap-v2-abis.json')


class UniswapV2PoolAPI(DexPoolAPI):

    def __init__(self, dex_id: str, address: ChecksumAddress, chain_id: int,
                 tokens: List[ChecksumAddress], pool_contract: Contract) -> None:
        super().__init__(dex_id=dex_id, chain_id=chain_id, address=address, tokens=tokens, pool_contract=pool_contract)

    def get_reserves(self) -> Dict[ChecksumAddress, Decimal]:
        res = self._contract.functions.getReserves().call()
        return {
            self.tokens[0]: Decimal(res[0]),
            self.tokens[1]: Decimal(res[1])
        }

    @staticmethod
    def build(config: DexPoolInfo, contract_loader: ContractLoader,
              pool_abi: list = None, **kwargs) -> 'UniswapV2PoolAPI':
        pool_abi = pool_abi or UNISWAP_V2_DEFAULTS['pool']
        return UniswapV2PoolAPI(
            dex_id=config.dex_id,
            address=config.address,
            chain_id=config.chain_id,
            tokens=config.tokens,
            pool_contract=contract_loader(config.chain_id, config.address, pool_abi)
        )


class UniswapV2API(DexAPI):

    def __init__(self, name: str, subtype: str, chain_id: int, trading_fee: Decimal, dex_id: str,
                 addresses: Dict[str, ChecksumAddress], contract_loader: ContractLoader,
                 pool_abi: list = None, router_abi: list = None, factory_abi: list = None) -> None:
        super().__init__(
            name=name, subtype=subtype, chain_id=chain_id, trading_fee=trading_fee,
            dex_id=dex_id, addresses=addresses, contract_loader=contract_loader
        )
        self._pool_abi = pool_abi or UNISWAP_V2_DEFAULTS['pool']
        router_abi = router_abi or UNISWAP_V2_DEFAULTS['router']
        factory_abi = factory_abi or UNISWAP_V2_DEFAULTS['factory']
        self.router: Contract = self._contract_loader(self.chain_id, addresses['router'], router_abi)
        self.factory: Contract = self._contract_loader(self.chain_id, addresses['factory'], factory_abi)

    def tradable(self, token0: ChecksumAddress, token1: ChecksumAddress) -> bool:
        raise NotImplementedError

    def quote(self, token0: ChecksumAddress, token1: ChecksumAddress, amount: int) -> Decimal:
        # resp = self.router.functions.getAmountsOut(amountIn=str(amount), path=[token0, token1]).call()
        resp = self.router.functions.getAmountsOut(amount, [token0, token1]).call()
        return Decimal(resp[-1])

    def get_pool_api(self, pool_info: DexPoolInfo) -> UniswapV2PoolAPI:
        pool_contract = self._contract_loader(self.chain_id, pool_info.address, self._pool_abi)
        return UniswapV2PoolAPI(
            dex_id=self.id,
            chain_id=self.chain_id,
            address=pool_info.address,
            tokens=pool_info.tokens,
            pool_contract=pool_contract
        )

    @staticmethod
    def build(config: DexInfo, contract_loader: ContractLoader, **kwargs) -> 'UniswapV2API':
        addresses = {
            'router': config.contracts['router'].address,
            'factory': config.contracts['factory'].address
        }
        return UniswapV2API(
            name=config.name, subtype=config.subtype, chain_id=config.chain_id, trading_fee=config.trading_fee,
            dex_id=config.id, addresses=addresses, contract_loader=contract_loader, pool_abi=config.pool_abi,
            router_abi=config.contracts['router'].abi, factory_abi=config.contracts['factory'].abi
        )


class UniswapV2DataLoader(DexDataLoader):
    BATCH_SIZE = 1000
    RESERVE_USD_GT = 100_000
    PAIRS_QUERY = """
    {{
      pairs(first: {batch_size}, skip: {skip_index}, where: {{reserveUSD_gt: {reserve_usd_gt}}}) {{
        id
        token0 {{
          id
        }}
        token1 {{
          id
        }}
      }}
    }}"""

    def _response_handler(self, data: dict, dex: str, chain_id: int) -> Tuple[List[DexPoolInfo], bool]:
        pools = data.get('data', {}).get('pairs')
        if not pools:
            return [], False
        pool_info = [
            DexPoolInfo(
                address=pool['id'],
                tokens=[pool['token0']['id'], pool['token1']['id']],
                dex_id=dex,
                chain_id=chain_id
            ) for pool in pools
        ]
        next_page = len(pools) == self.BATCH_SIZE
        return pool_info, next_page

    def load_data(self, dex_info: DexInfo, repo: DexRepo) -> None:
        if not dex_info.subgraph_url:
            log.info(__name__, f'No subgraph url for {dex_info.name} on chain {dex_info.chain_id}')
            return
        next_page = True
        skip_index = 0
        while next_page:
            query = self.PAIRS_QUERY.format(
                reserve_usd_gt=self.RESERVE_USD_GT,
                batch_size=self.BATCH_SIZE,
                skip_index=skip_index
            )
            data = graphql.query(dex_info.subgraph_url, query)
            pools, next_page = self._response_handler(data, dex=dex_info.id, chain_id=dex_info.chain_id)
            skip_index += self.BATCH_SIZE
            if pools:
                log.info(__name__, f'Saving {len(pools)} pools for {dex_info.name} on chain {dex_info.chain_id}')
                repo.save_pools(pools)


UNISWAP_V2_PACKAGE = DexPackage(
    subtype='UniswapV2',
    dex_api=UniswapV2API,
    pool_api=UniswapV2PoolAPI,
    data_loader=UniswapV2DataLoader
)
