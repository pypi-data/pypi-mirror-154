from typing import List
from ._dtypes import DexInfo, DexPoolInfo, SwapRoute, Swap
from ._adaptors import DexAPI, DexPoolAPI
from ._repo import DexRepo
from . import _config
from deanerfi.w3.api import get_contract, get_token
from web3.exceptions import BadFunctionCallOutput
from deanerfi.common.log import api as log


def get_dex_repo() -> DexRepo:
    return _config.DEX_REPO


def set_dex_repo(dex_repo: DexRepo) -> None:
    _config.DEX_REPO = dex_repo


def get_dex_configs(chain_id: int = None, subtype: str = None) -> List[DexInfo]:
    """Returns the DexInfos that are configured in the DexRepo"""
    return _config.DEX_REPO.get_configs(chain_id=chain_id, subtype=subtype)


def build_dex(dex_config: DexInfo) -> DexAPI:
    """Builder function that takes the DexInfo and returns the DexAPI"""
    return _config.DEX_PKGS[dex_config.subtype].dex_api.build(config=dex_config, contract_loader=get_contract)


def update_dex_pools(dex_config: DexInfo) -> None:
    """Updates the available pools for the given dex in the DexRepo"""
    data_loader = _config.DEX_PKGS[dex_config.subtype].data_loader()
    log.info(__name__, f'Updating Pools for {dex_config.name} on Chain #{dex_config.chain_id}')
    data_loader.load_data(dex_info=dex_config, repo=get_dex_repo())


def update_pools() -> None:
    """Updates all known dexs information in the DexRepo"""
    for dex_config in get_dex_configs():
        update_dex_pools(dex_config=dex_config)


def get_dex_config(dex_id: str) -> DexInfo:
    return _config.DEX_REPO.get_config(dex_id=dex_id)


def get_pool_api(pool_info: DexPoolInfo) -> DexPoolAPI:
    dex_config = get_dex_config(pool_info.dex_id)
    return _config.DEX_PKGS[dex_config.subtype].pool_api.build(
        config=pool_info,
        pool_abi=dex_config.pool_abi,
        contract_loader=get_contract
    )


def print_swap_route(swap_route: SwapRoute, chain_id: int) -> None:
    dex_repo = get_dex_repo()
    token_in = get_token(chain_id=chain_id, address=swap_route.token_in)
    token_out = get_token(chain_id=chain_id, address=swap_route.token_out)
    print(
        f'Swap Route: {token_in.from_wei(swap_route.amount_in)} {token_in.symbol} -> {token_out.from_wei(swap_route.amount_out)} {token_out.symbol}')
    try:
        for swap in swap_route.route:
            pool_info = dex_repo.get_pool_info(chain_id=chain_id, address=swap.pool_address)
            token_in = get_token(chain_id=chain_id, address=swap.token_in)
            token_out = get_token(chain_id=chain_id, address=swap.token_out)
            print(f' - {pool_info.dex_id}: {swap.amount_in} {token_in.symbol} -> {swap.amount_out} {token_out.symbol}')
    except BadFunctionCallOutput:
        log.error(__name__, f'BadFunctionCallOutput:', data=swap_route)


def quote_swap(swap: Swap, chain_id: int) -> None:
    pool_info = _config.DEX_REPO.get_pool_info(chain_id=chain_id, address=swap.pool_address)
    dex_api = build_dex(get_dex_config(pool_info.dex_id))
    swap.amount_out = dex_api.quote(token0=swap.token_in, token1=swap.token_out, amount=int(swap.amount_in))


def quote_route(swap_route: SwapRoute, chain_id: int) -> None:
    len_swaps = len(swap_route.route) - 1
    for i, swap in enumerate(swap_route.route):
        quote_swap(swap, chain_id)
        if i != len_swaps:
            swap_route.route[i + 1].amount_in = swap_route.route[i].amount_out
