import asyncio
from dataclasses import dataclass, field
from typing import List
from eth_typing import ChecksumAddress

from deanerfi.dex import DexPoolAPI
from deanerfi.common.msgbus import MessageBus, Event, Command, Message
from decimal import Decimal


@dataclass
class SwapEvent(Event):
    dex_id: str
    chain_id: int
    pool_address: ChecksumAddress
    name: str = field(init=False, default='swap_event')


@dataclass
class UpdateReserves(Command):
    dex_id: str
    chain_id: int
    pool_address: ChecksumAddress
    name: str = field(init=False, default='update_reserves')


@dataclass
class ReservesUpdated(Event):
    dex_id: str
    chain_id: int
    pool_address: ChecksumAddress
    token0: str
    token1: str
    token0_res: Decimal
    token1_res: Decimal
    price: Decimal = None
    name: str = field(init=False, default='update_reserves')

    def __post_init__(self):
        self.price = self.token0_res / self.token1_res


async def listen_for_swaps(pool_api: DexPoolAPI, msg_bus: MessageBus):
    event_filter = pool_api._contract.events.Swap.createFilter(fromBlock='latest')
    while True:
        for swap in event_filter.get_new_entries():
            msg_bus.send_msg(SwapEvent(
                dex_id=pool_api.dex_id, chain_id=pool_api.chain_id, pool_address=pool_api.address
            ))
            msg_bus.send_msg(UpdateReserves(
                dex_id=pool_api.dex_id, chain_id=pool_api.chain_id, pool_address=pool_api.address
            ))
        msg_bus.process_msgs()
        await asyncio.sleep(0.001)


def update_reserves(cmd: UpdateReserves) -> List[Message]:
    dex_repo = deanerfi.dex.api.get_dex_repo()
    pool_info = dex_repo.get_pool_info(chain_id=cmd.chain_id, address=cmd.pool_address)
    pool_api = deanerfi.dex.api.get_pool_api(pool_info)
    pool_reserves = pool_api.get_reserves()
    token_repo = deanerfi.w3.api.get_token_repo()
    tokens = [token_repo.get_token(chain_id=cmd.chain_id, address=addr) for addr in pool_info.tokens]
    return [
        ReservesUpdated(
            dex_id=cmd.dex_id, chain_id=cmd.chain_id, pool_address=cmd.pool_address, token0=tokens[0].symbol,
            token1=tokens[1].symbol, token0_res=tokens[0].from_wei(pool_reserves[tokens[0].address]),
            token1_res=tokens[1].from_wei(pool_reserves[tokens[1].address])
        )
    ]


def pub_dex_trades(chain_id: int, tokens: List[ChecksumAddress], msg_bus: MessageBus) -> None:
    dex_repo = deanerfi.dex.api.get_dex_repo()

    pools_info = dex_repo.pools_w_tokens(chain_id=chain_id, tokens=tokens)
    watch_pools = [deanerfi.dex.api.get_pool_api(pool_info=p_info) for p_info in pools_info]
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                *[listen_for_swaps(pool, msg_bus) for pool in watch_pools]
            )
        )
    finally:
        loop.close()
