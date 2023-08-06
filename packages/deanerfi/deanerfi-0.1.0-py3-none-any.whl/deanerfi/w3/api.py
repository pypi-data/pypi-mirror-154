from typing import List

from web3.contract import Contract

from . import _config
from ._adaptor import Web3Wrapper
from ._dtypes import TokenInfo, ChainInfo
from ._repos import ChainRepo, TokenRepo
from deanerfi.utils.w3 import cs_addr


def get_chain_repo() -> ChainRepo:
    return _config.CHAIN_REPO


def set_chain_repo(chain_repo: ChainRepo) -> None:
    _config.CHAIN_REPO = chain_repo


def get_token_repo() -> TokenRepo:
    return _config.TOKEN_REPO


def set_token_repo(token_repo: TokenRepo) -> None:
    _config.TOKEN_REPO = token_repo


def get_chain_info(chain_id: int) -> ChainInfo:
    chain_repo = get_chain_repo()
    return chain_repo.get(chain_id=chain_id)


def get_token(address: str, chain_id: int, save: bool = True) -> TokenInfo:
    address = cs_addr(address)
    token_repo = get_token_repo()
    token = token_repo.get_token(chain_id, address)
    if token:
        # CONFIG.LOGGER.info(__name__, 'TokenInfo found in TokenRepo', _token.to_dict())
        return token
    chain_info = get_chain_info(chain_id=chain_id)
    # CONFIG.LOGGER.info(__name__, 'ChainInfo: ', _chain)
    with Web3Wrapper.from_chain_info(chain_info) as w3_uow:
        token = w3_uow.get_token_info(address)
        # CONFIG.LOGGER.info(__name__, 'TokenInfo not found in TokenRepo. Loaded from contract', _token.to_dict())
    if save:
        token_repo.save(token)
    return token


def get_contract(chain_id: int, address: str, abi: list) -> Contract:
    chain_info = get_chain_info(chain_id=chain_id)
    address = cs_addr(address)
    with Web3Wrapper.from_chain_info(chain_info) as w3_uow:
        contract = w3_uow.get_contract(address=address, abi=abi)
    return contract


def get_wl_tokens(chain_id: int) -> List[TokenInfo]:
    return _config.TOKEN_REPO.get_wl_token(chain_id=chain_id)
