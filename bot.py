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

    logging.info("Handlers registered.")


def register_all_middlewares() -> None:
    logging.info("Middlewares registered.")


def register_all_filters() -> None:
    logging.info("Filters registered.")


async def on_startup() -> None:
    register_all_handlers()
    register_all_middlewares()
    register_all_filters()


async def on_shutdown(dispatcher: Dispatcher) -> None:
    await dispatcher.storage.close()
    logging.info("Storage closed.")
    logging.info("Bot stopped.")


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        filename="bot.log",
        format="%(asctime)s :: %(levelname)s :: %(module)s.%(funcName)s :: %(lineno)d :: %(message)s",
        filemode="w",
    )
    asyncio.run(main())
