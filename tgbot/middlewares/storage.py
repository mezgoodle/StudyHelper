from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from tgbot.misc.storage import Storage


class StorageMiddleware(BaseMiddleware):
    def __init__(self, storage_instance: Storage) -> None:
        self.storage = storage_instance

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        data["storage"] = self.storage
        return await handler(event, data)
