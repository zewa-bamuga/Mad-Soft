import asyncio
import functools
from collections.abc import Callable
from typing import Any

import typer
from loguru import logger

import app.domain
from app.containers import Container
from app.domain.common.schemas import MemeCreate
from a8t_tools.db.exceptions import DatabaseError


def async_to_sync(fn: Callable[..., Any]) -> Callable[..., Any]:
    if not asyncio.iscoroutinefunction(fn):
        return fn

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        coro = fn(*args, **kwargs)
        return asyncio.get_event_loop().run_until_complete(coro)

    return wrapper


def create_container() -> Container:
    container = Container()
    container.wire(packages=[app.domain])
    container.init_resources()
    return container


container = create_container()
typer_app = typer.Typer()


@typer_app.command()
@async_to_sync
async def noop() -> None:
    pass


@typer_app.command()
@async_to_sync
async def create_meme(
        description: str = typer.Argument(...),
) -> None:
    command = container.meme.create_meme()
    try:
        await command(
            MemeCreate(
                description=description,
            ),
        )
    except DatabaseError as err:
        logger.warning(f"Meme creation error: {err}")
