from pathlib import Path

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentTypes, Message

from loader import dp
from tgbot.misc.import_students import receive_file


@dp.message_handler(Command(["add_students"]))
async def add_students(message: Message, state: FSMContext) -> Message:
    await state.set_state("wait_for_file")
    # TODO: send template file
    return await message.answer(
        "Send file with students' data. Formats: .csv, .xlsx, .xls"
    )


@dp.message_handler(state="wait_for_file", content_types=ContentTypes.DOCUMENT)
async def process_file(message: Message, state: FSMContext) -> Message:
    if message.document:
        if message.document.file_name.lower().endswith((".csv", ".xlsx", ".xls")):
            await state.finish()
            path_to_download = Path().joinpath("files", "imports")
            path_to_download.mkdir(parents=True, exist_ok=True)
            path_to_download = path_to_download.joinpath(message.document.file_name)
            path = await message.document.download(destination_file=path_to_download)
            receive_file(path)
            return await message.answer("File received")
        return await message.answer(
            "You should send file with students' data. Formats: .csv, .xlsx, .xls"
        )
    return await message.answer(
        "You should send file with students' data. Formats: .csv, .xlsx, .xls"
    )
