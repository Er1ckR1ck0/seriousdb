from typing import Annotated
from fastapi import Depends

from .cache import Cache, cache

def get_cache() -> Cache:
    return cache

CacheDep = Annotated[Cache, Depends(get_cache)]