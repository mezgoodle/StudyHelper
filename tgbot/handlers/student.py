from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.filters.student import IsStudentFilter
from tgbot.misc.database import Database
from tgbot.models.models import Student

router = Router()
router.message.filter(IsStudentFilter())
dp.include_router(router)


@router.message(Command("is_student"))
async def check_student(message: Message) -> None:
    return await message.answer("You are a student!")


@router.message(Command("my_subjects"))
async def get_subjects(
    message: Message, db: Database, student: Student
) -> None:
    if subjects := await db.get_student_subjects(student):
        print(subjects)
        return await message.answer(
            "Here are your subjects:",
        )
    return await message.answer("You don't have any subjects!")
