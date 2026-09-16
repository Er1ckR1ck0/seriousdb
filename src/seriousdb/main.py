from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import BackgroundTasks, FastAPI, HTTPException, Query

from .cache import cache
from .config import DB_FILE
from .deps import CacheDeps
from .error_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    cache.load(DB_FILE)
    yield


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)


@app.put("/db")
def put(
    key: Annotated[str, Query(min_length=1)],
    value: str,
    background_tasks: BackgroundTasks,
    cache: CacheDeps,
) -> str:
    cache.insert(key, value)
    background_tasks.add_task(cache.flush)
    return value


@app.get("/db")
def get(key: str, cache: CacheDeps) -> str:
    return cache.select(key)


@app.head("/db")
async def head(key: str, cache: CacheDeps) -> str:
    return cache.select(key)


@app.get("/db/all")
def get_all(cache: CacheDeps) -> dict[str, str]:
    return cache.get_all()


@app.delete("/db/all")
def delete_all(background_tasks: BackgroundTasks, cache: CacheDeps):
    cache.clear()
    background_tasks.add_task(cache.flush)


@app.delete("/db")
def delete(
    key: str,
    background_tasks: BackgroundTasks,
    cache: CacheDeps,
):
    value = cache.delete(key)
    background_tasks.add_task(cache.flush)
    return value


@app.get("/health")
def health(cache: CacheDeps):
    if cache.db is None:
        raise HTTPException(status_code=503, detail="Service unavailable")
    return {"status": "ok"}
