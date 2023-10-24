from json import loads

from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload

from loader import dp
from tgbot.misc.database import Database

router = Router()
dp.include_router(router)


@router.message(Command("register_teacher"))
async def register_as_teacher(message: Message, db: Database) -> None:
    if await db.create_teacher(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name,
    ):
        return await message.answer(
            "You are registered as a teacher. To check it, type /is_teacher"
        )
    return await message.answer("Error while registering as a teacher")


@router.message(Command("register_student"))
async def register_as_student(message: Message, db: Database) -> None:
    if await db.create_student(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name,
    ):
        return await message.answer(
            "You are registered as a student. To check it, type /is_student"
        )
    return await message.answer("Error while registering as a student")


@router.message(CommandStart(deep_link=True))
async def handler(message: Message, command: CommandObject) -> Message:
    args = command.args
    payload = decode_payload(args)
    data = loads(payload)
    print(data)
    return await message.answer(f"Your payload: {payload}")
