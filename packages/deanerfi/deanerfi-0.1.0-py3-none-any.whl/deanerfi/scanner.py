from typing import Protocol
import json
from typing import Optional

import requests
from web3 import Web3


class ChainScanner(Protocol):
    def get_tx(self, tx_hash):
        pass


class EtherScan:
    """Chain scanner for etherscan.com clones"""

    def __init__(self, url: str, api_key: str) -> None:
        self.base_url = url
        self.api_key = api_key

    def _make_req(self, params: dict) -> Optional[dict]:
        resp = requests.get(self.base_url, params=params)
        if resp.status_code != 200:
            return None
        return resp.json()

    def get_abi(self, addr: str) -> Optional[list]:
        params = {
            'module': 'contract',
            'action': 'getabi',
            'address': addr,
            'apikey': self.api_key
        }
        abi = self._make_req(params).get('result')
        if not abi:
            return None
        return json.loads(abi)

    def get_txs(self, addr: str) -> Optional[list]:
        params = {
            'module': 'account',
            'action': 'txlist',
            'address': addr,
            'startblock': 1,
            'endblock': 99999999,
            'sort': 'asc',
            'apikey': self.api_key
        }
        resp = self._make_req(params)
        if resp['message'] == 'OK':
            # return [EthScannerTx(**tx) for tx in resp['result']]
            for tx in resp['result']:
                tx['to'] = Web3.toChecksumAddress(tx['to'])
                tx['from'] = Web3.toChecksumAddress(tx['from'])
            return resp['result']
        else:
            return resp

    def get_internal_txs(self, tx_hash: str):
        params = {
            'module': 'account',
            'action': 'txlistinternal',
            'txhash': tx_hash,
            'apikey': self.api_key
        }
        resp = self._make_req(params)
        if resp['message'] == 'OK':
            return resp['result']
        else:
            return resp

    def get_token_txs(self, addr: str):
        params = {
            'module': 'account',
            'action': 'tokentx',
            'address': addr,
            'startblock': 1,
            'endblock': 99999999,
            'sort': 'asc',
            'apikey': self.api_key
        }
        resp = self._make_req(params)
        if resp['message'] == 'OK':
            return resp['result']
        else:
            return resp
