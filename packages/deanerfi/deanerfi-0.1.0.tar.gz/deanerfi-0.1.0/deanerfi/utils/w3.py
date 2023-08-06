from eth_typing import ChecksumAddress
from web3 import Web3


def cs_addr(address: str) -> ChecksumAddress:
    """Simple wrapper function that takes a string and returns a ChecksumAddress"""
    return Web3.toChecksumAddress(address)

