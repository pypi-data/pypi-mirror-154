from __future__ import annotations

from typing import TYPE_CHECKING, Any, Coroutine

from asgiref.sync import async_to_sync

from .exceptions import BadRequest, NotAuthorized, NotFound
from .sessions import sessions


# async def reflect(*args, **kwargs) -> Coroutine[Any]:
async def reflect(*args, **kwargs):
    return await sessions["global"].reflect(*args, **kwargs)


reflect_sync = async_to_sync(reflect)
