from json import loads

from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.deep_linking import decode_payload

from loader import dp
from tgbot.misc.database import Database
from tgbot.misc.texts import STUDENT_HELP_TEXT, TEACHER_HELP_TEXT
from tgbot.misc.utils import utils

router = Router()
dp.include_router(router)


@router.message(Command("register_teacher"))
async def register_as_teacher(message: Message, db: Database) -> Message:
    if await db.create_teacher(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name,
    ):
        await message.answer(
            "You are registered as a teacher. To check it, type /is_teacher"
        )
        return await message.answer(TEACHER_HELP_TEXT)
    return await message.answer("Error while registering as a teacher")


@router.message(Command("register_student"))
async def register_as_student(message: Message, db: Database) -> Message:
    if await db.create_student(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name,
    ):
        await message.answer(
            "You are registered as a student. To check it, type /is_student"
        )
        return await message.answer(STUDENT_HELP_TEXT)
    return await message.answer("Error while registering as a student")


@router.message(Command(commands=["cancel"], ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext) -> Message:
    await state.clear()
    return await message.answer(
        text="Your state has been cleared", reply_markup=ReplyKeyboardRemove()
    )


@router.message(CommandStart())
async def start_handler(message: Message) -> Message:
    return await message.answer(
        "Hello, I'm Study Helper bot! To see available commands, type /help"
    )


@router.message(Command("help"))
async def help_handler(message: Message) -> Message:
    return await message.answer(
        "Available commands: /register_student, /register_teacher\nAdministator: @sylvenis"
    )


@router.message(CommandStart(deep_link=True))
async def deep_link_handler(
    message: Message, command: CommandObject, db: Database, state: FSMContext
) -> Message:
    args = command.args
    payload = decode_payload(args)
    data: dict = loads(payload)
    if (key := data.get("key")) and key in utils:
        return await utils.get(key)(message, data, db, state)
    return await message.answer("Unknown command")
