from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp


@dp.message_handler(Command(["echo"]))
async def echo(message: Message) -> Message:
    await message.answer(message.text)
