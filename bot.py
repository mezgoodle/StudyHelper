import asyncio
import logging

from aiogram import Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from loader import bot, dp
from tgbot.config import Settings, config
from tgbot.middlewares.settings import ConfigMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware


def register_all_handlers() -> None:
    from tgbot import handlers  # noqa: F401

    logging.info("Handlers registered.")


def register_global_middlewares(dp: Dispatcher, config: Settings):
    middlewares = [
        ConfigMiddleware(config),
        ThrottlingMiddleware(),
        # DatabaseMiddleware(session_pool),
    ]

    for middleware in middlewares:
        dp.message.outer_middleware(middleware)
        dp.callback_query.outer_middleware(middleware)

    dp.callback_query.middleware(
        CallbackAnswerMiddleware(pre=True, text="Ready!", show_alert=True)
    )


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
        format="%(asctime)s :: %(levelname)s :: %(module)s.%(funcName)s :: %(lineno)d :: %(message)s",  # noqa: E501
        filemode="w",
    )
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Bot stopped!")
