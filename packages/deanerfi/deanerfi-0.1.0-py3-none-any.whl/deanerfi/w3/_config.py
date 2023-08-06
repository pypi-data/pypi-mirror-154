from os import environ

from ._repos import (
    ContractRepo, LocalContractRepo, MongoDBContractRepo,
    ChainRepo, LocalChainRepo, MongoDBChainRepo,
    TokenRepo, LocalTokenRepo, MongoDBTokenRepo
)


local_repo_path = environ.get('LOCAL_REPO_PATH')

token_repo_fp = f'{local_repo_path}/token-repo.json' if local_repo_path else None
chain_repo_fp = f'{local_repo_path}/chain-repo.json' if local_repo_path else None

TOKEN_REPO: TokenRepo = LocalTokenRepo(file_path=token_repo_fp)
CHAIN_REPO: ChainRepo = LocalChainRepo(file_path=chain_repo_fp)
