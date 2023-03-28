from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentTypes, Message

from loader import dp


@dp.message_handler(Command(["add_students"]))
async def add_students(message: Message, state: FSMContext) -> Message:
    await state.set_state("wait_for_file")
    return await message.answer(
        "Send file with students' data. Formats: .csv, .xlsx, .xls"
    )


@dp.message_handler(state="wait_for_file", content_types=ContentTypes.DOCUMENT)
async def process_file(message: Message, state: FSMContext) -> Message:
    await state.finish()
    return await message.answer("File received")
