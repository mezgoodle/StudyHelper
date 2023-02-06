from aiogram.types import Message

from loader import dp


@dp.message_handler()
async def echo(message: Message) -> Message:
    engine = message.bot.get("engine")
    print(engine, type(engine))
    await message.answer(message.text)
