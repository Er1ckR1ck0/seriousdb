from typing import Callable

from seriousdb import deps, main
from seriousdb.cache import Cache

def get_deps_func() -> Callable[[], Cache]:
    return getattr(main, "get_cache", deps.get_cache)