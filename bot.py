import asyncio
import logging

from aiogram import Dispatcher

from loader import bot, dp
from tgbot.config import Settings, config
from tgbot.middlewares.settings import ConfigMiddleware


def register_all_handlers() -> None:
    from tgbot import handlers

    logging.info("Handlers registered.")


def register_global_middlewares(dp: Dispatcher, config: Settings):
    middlewares = [
        ConfigMiddleware(config),
        # DatabaseMiddleware(session_pool),
    ]

    for middleware in middlewares:
        dp.message.outer_middleware(middleware)
        dp.callback_query.outer_middleware(middleware)


async def on_startup(dispatcher: Dispatcher) -> None:
    register_all_handlers()
    register_global_middlewares(dispatcher, config)


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
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Bot stopped!")
