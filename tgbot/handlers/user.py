from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from loader import dp
from tgbot.keyboards.reply.reg_keyboard import create_markup
from tgbot.middlewares.throttling import rate_limit
from tgbot.states.states import Example


@dp.message_handler(CommandStart(), state="*")
@rate_limit(5, "start")
async def user_command(message: Message) -> Message:
    await Example.first()
    markup = create_markup()
    await message.reply("Hello, user!", reply_markup=markup)
