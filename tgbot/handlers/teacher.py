from pathlib import Path

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentTypes, InputFile, Message
from aiogram.utils.markdown import hbold

from loader import dp
from tgbot.misc.import_students import parse_students_from_file
from tgbot.misc.utils import check_extension, delete_file, download_file
from tgbot.models.database import Database
from tgbot.states.states import File, Subject


@dp.message_handler(Command(["register_teacher"]))
async def register_teacher(message: Message) -> Message:
    db: Database = message.bot.get("db")
    user = message.from_user
    if db.get_teacher(message.from_user.id):
        return await message.answer("You are already registered as teacher")
    if db.create_teacher(
        name=user.full_name, telegram_id=user.id, username=user.username
    ):
        return await message.answer("You are registered as teacher")
    return await message.answer("Something went wrong")


@dp.message_handler(Command(["is_teacher"]), is_teacher=True)
async def is_teacher(message: Message) -> Message:
    return await message.answer("Yes, you are the teacher!")


@dp.message_handler(Command(["is_teacher"]))
async def is_not_teacher(message: Message) -> Message:
    return await message.answer("No, you are not the teacher!")


@dp.message_handler(Command(["add_subject"]), is_teacher=True)
async def add_subject(message: Message) -> Message:
    await Subject.first()
    return await message.answer("Send subject name")


@dp.message_handler(state=Subject.name)
async def answer_subject_name(message: Message, state: FSMContext) -> Message:
    await state.update_data(subject_name=message.text)
    await Subject.next()
    return await message.answer("Send group name")


@dp.message_handler(state=Subject.group)
async def answer_group_name(message: Message, state: FSMContext) -> Message:
    data = await state.get_data()
    db: Database = message.bot.get("db")
    if db.create_subject(
        data["subject_name"], message.from_user.id, message.text
    ):
        await state.finish()
        return await message.answer(
            f"Subject {hbold(data['subject_name'])} was added"
        )
    await state.finish()
    return await message.answer(
        f"Subject {data['subject_name']} already exists"
    )


@dp.message_handler(Command(["add_students"]))
async def add_students(message: Message) -> Message:
    await File.first()
    path_to_file = Path().joinpath("files", "exports", "example.xlsx")
    await message.answer_document(InputFile(path_to_file), caption="Example")
    return await message.answer(
        "Send file with students' data as in the example. Formats: .csv, .xlsx, .xls"
    )


@dp.message_handler(state=File.file, content_types=ContentTypes.DOCUMENT)
async def process_file(message: Message, state: FSMContext) -> Message:
    await state.finish()
    if message.document:
        try:
            file_name = message.document.file_name
            check_extension(file_name)
            downloaded_path = await download_file(file_name, message)
            db = message.bot.get("db")
            number_of_students = await parse_students_from_file(
                downloaded_path, db, message
            )
            delete_file(downloaded_path)
        except Exception as error_message:
            return await message.answer(error_message)
        return await message.answer(
            f"{number_of_students} students were added."
        )
    return await message.answer(
        "You should send file with students' data. Formats: .csv, .xlsx, .xls"
    )
