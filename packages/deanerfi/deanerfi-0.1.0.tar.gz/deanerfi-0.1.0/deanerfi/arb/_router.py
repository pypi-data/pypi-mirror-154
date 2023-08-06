from typing import Protocol, List
from deanerfi.dex import SwapRoute, DexPoolInfo, Swap
from eth_typing import ChecksumAddress
import networkx as nx

from deanerfi.utils.w3 import cs_addr


class TradeRouter(Protocol):

    def route(self, token0: ChecksumAddress, token1: ChecksumAddress, max_swaps: int = 2) -> List[SwapRoute]:
        """Returns all possible swap routes. Routes initialized with 0 tokens traded"""
        pass


class TokenGraphTradeRouter:
    """Trades Router that utilizes a graph with Tokens as nodes and pools as edges"""

    def __init__(self, pools: List[DexPoolInfo] = None):
        self.graph = nx.MultiGraph()
        if pools:
            self.add_pools(pools)

    def route(self, token0: ChecksumAddress, token1: ChecksumAddress, max_swaps: int = 2) -> List[SwapRoute]:
        paths = nx.all_simple_edge_paths(self.graph, source=token0, target=token1, cutoff=max_swaps)
        if not paths:
            return []
        return [self.parse_path(path) for path in paths]

    def loop_route(self, token0: ChecksumAddress, max_swaps: int = 2) -> List[SwapRoute]:
        start_paths = self.route(token0=token0, token1=self.graph.neighbors(token0), max_swaps=max_swaps - 1)
        paths = []
        for path in start_paths:
            ret_paths = self.route(token0=path.token_out, token1=path.token_in, max_swaps=1)
            for ret_path in ret_paths:
                # if path.route[0] != ret_path.route[0]:
                paths.append(
                    SwapRoute(route=path.route + ret_path.route)
                )
        return paths

    @staticmethod
    def parse_path(path: List[ChecksumAddress]) -> SwapRoute:
        swap_route = SwapRoute()
        for swap in path:
            swap_route.add_swap(
                Swap(
                    token_in=cs_addr(swap[0]),
                    token_out=cs_addr(swap[1]),
                    pool_address=cs_addr(swap[2]),
                )
            )
        return swap_route

    def add_node(self, token_addr: ChecksumAddress) -> None:
        if not self.graph.has_node(token_addr):
            self.graph.add_node(token_addr)

    def add_nodes(self, token_addrs: List[ChecksumAddress]) -> None:
        for token_addr in token_addrs:
            self.add_node(token_addr)

    def add_pool(self, pool: DexPoolInfo) -> None:
        self.add_nodes(pool.tokens)
        self.graph.add_edge(pool.tokens[0], pool.tokens[1], pool.address)

    def add_pools(self, pools: List[DexPoolInfo]) -> None:
        for pool in pools:
            self.add_pool(pool)
