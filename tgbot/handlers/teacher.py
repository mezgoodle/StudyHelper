from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.filters.teacher import IsTeacherFilter

router = Router()
router.message.filter(IsTeacherFilter())
dp.include_router(router)


@router.message(Command("is_teacher"))
async def check_teacher(message: Message) -> None:
    return await message.answer("You are a teacher!")
