from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.models.database import Database


@dp.message_handler(Command(["register_student"]))
async def register_student(message: Message, state: FSMContext) -> Message:
    await state.set_state("wait_for_group")
    return await message.answer("Send your group")


@dp.message_handler(state="wait_for_group")
async def process_group(message: Message, state: FSMContext) -> Message:
    await state.finish()
    db: Database = message.bot.get("db")
    user = message.from_user
    if db.get_student(message.from_user.id):
        return await message.answer("You are already registered as student")
    if db.create_student(
        name=user.full_name,
        telegram_id=user.id,
        username=user.username,
        group=message.text,
    ):
        return await message.answer("You are registered as student")
    return await message.answer("Something went wrong")
