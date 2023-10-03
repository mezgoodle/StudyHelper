from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.misc.database import Database

router = Router()
dp.include_router(router)


@router.message(Command("teachers"))
async def get_teachers_handler(message: Message, db: Database) -> None:
    teachers = await db.get_teachers()
    print(teachers)
    return await message.answer("Teachers are printed")


@router.message(Command("students"))
async def get_students_handler(message: Message, db: Database) -> None:
    students = await db.get_students()
    print(students)
    return await message.answer("Students are printed")


@router.message(Command("create_teacher"))
async def create_teacher_handler(message: Message, db: Database) -> None:
    teacher = await db.create_teacher(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name,
    )
    print(teacher)
    return await message.answer("Teacher created")


@router.message(Command("create_student"))
async def create_student_handler(message: Message, db: Database) -> None:
    student = await db.create_student(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name,
    )
    print(student)
    return await message.answer("Student created")
