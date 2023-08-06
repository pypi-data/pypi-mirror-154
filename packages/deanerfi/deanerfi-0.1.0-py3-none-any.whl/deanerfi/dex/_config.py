from os import environ
from typing import Dict

from ._adaptors import DexPackage, DexRepo
from ._repo import LocalDexRepo
from ._uniswap import UNISWAP_V2_PACKAGE

local_repo_path = environ.get('LOCAL_REPO_PATH')

dex_repo_fp = f'{local_repo_path}/dex-repo.json' if local_repo_path else None

DEX_PKGS: Dict[str, DexPackage] = {
    UNISWAP_V2_PACKAGE.subtype: UNISWAP_V2_PACKAGE
}

DEX_REPO: DexRepo = LocalDexRepo(file_path=dex_repo_fp)
