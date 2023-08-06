from deanerfi import w3, dex


def mongo_repos():
    """Sets up the mongo repositories for the token, chain, and dex repositories."""
    w3.api.set_token_repo(w3.MongoDBTokenRepo())
    w3.api.set_chain_repo(w3.MongoDBChainRepo())
    dex.api.set_dex_repo(dex.MongoDBDexRepo())
