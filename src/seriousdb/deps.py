from typing import Annotated

from fastapi import Depends

from .cache import Cache, cache


def get_cache() -> Cache:
    return cache

CacheDeps = Annotated[Cache, Depends(get_cache)]