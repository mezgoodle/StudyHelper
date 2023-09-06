import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from loader import bot, dp


def register_all_handlers() -> None:
    from tgbot import handlers


async def on_startup() -> None:
    register_all_handlers()


async def main() -> None:
    dp.startup.register(on_startup)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
