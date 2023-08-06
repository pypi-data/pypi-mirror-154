from deanerfi import w3, dex
from deanerfi.arb import TokenGraphTradeRouter

chain_id = 250

# dex.api.set_dex_repo(dex.MongoDBDexRepo())
# w3.api.set_token_repo(w3.MongoDBTokenRepo())
#
# dex_repo = dex.api.get_dex_repo()
# pool_infos = dex_repo.chain_pools(chain_id)
#
# router = TokenGraphTradeRouter(
#     pools=pool_infos
# )
#
# token0 = w3.api.get_token(address='0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83', chain_id=chain_id)
# WAVAX = w3.api.get_token(address='0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7', chain_id=chain_id)

# routes = router.route(
#     token0=USDC.address,
#     token1=WAVAX.address,
#     max_swaps=1
# )
#
# routes = router.loop_route(
#     token0=token0.address,
#     max_swaps=3
# )
#
# for swap_route in routes:
#     swap_route.route[0].amount_in = token0.to_wei(100)
#     dex.api.quote_route(swap_route, chain_id)
#     dex.api.print_swap_route(swap_route, chain_id=chain_id)



