from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract
from web3.middleware import geth_poa_middleware

from ._dtypes import ChainInfo, TokenInfo
from deanerfi.utils.data import _load_pkg_data

ERC20_ABI = _load_pkg_data('erc20-abi.json')


class Web3Wrapper:
    """Implementation of Web3Handler abstraction for common web3 tasks"""

    def __init__(self, chain_id: int, rpc_url: str, inject_middleware: bool, name: str = None,
                 symbol: str = None) -> None:
        self.chain_id = chain_id
        self.name = name
        self.symbol = symbol
        self._w3 = Web3(
            Web3.HTTPProvider(rpc_url)
        )
        if inject_middleware:
            self._w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def __enter__(self) -> 'Web3Wrapper':
        return self

    def __exit__(self, error: Exception, value: object, traceback: object) -> None:
        pass

    def get_contract(self, address: ChecksumAddress, abi: list) -> Contract:
        return self._w3.eth.contract(address=address, abi=abi)

    def get_token_info(self, address: ChecksumAddress) -> TokenInfo:
        token_contract = self.get_contract(address, ERC20_ABI)
        return TokenInfo(
            symbol=token_contract.functions.symbol().call(),
            name=token_contract.functions.name().call(),
            address=address,
            chain_id=self.chain_id,
            decimals=token_contract.functions.decimals().call(),
        )

    @staticmethod
    def from_chain_info(chain_info: ChainInfo) -> 'Web3Wrapper':
        return Web3Wrapper(
            chain_id=chain_info.id,
            rpc_url=chain_info.rpc,
            inject_middleware=chain_info.inject_middleware,
            name=chain_info.name,
            symbol=chain_info.symbol
        )
