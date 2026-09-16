from seriousdb import deps, main

def get_deps_func():
    return getattr(main, "get_cache", deps.get_cache)