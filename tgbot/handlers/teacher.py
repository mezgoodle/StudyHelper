from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from loader import dp
from tgbot.filters.teacher import IsTeacherFilter
from tgbot.keyboards.reply.options_keyboard import options_keyboard
from tgbot.misc.database import Database
from tgbot.misc.utils import create_subject_message
from tgbot.models.models import Teacher
from tgbot.states.states import Options, Subject

router = Router()
router.message.filter(IsTeacherFilter())
dp.include_router(router)


@router.message(Command("is_teacher"))
async def check_teacher(message: Message) -> None:
    return await message.answer("You are a teacher!")


@router.message(Command("create_subject"))
async def create_subject(message: Message, state: FSMContext) -> None:
    await state.set_state(Subject.name)
    return await message.answer("Write a name for subject name")


@router.message(Subject.name)
async def set_subject_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Subject.description)
    return await message.answer("Write a description for subject")


@router.message(Subject.description)
async def set_subject_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(Subject.drive_link)
    return await message.answer("Write a google drive link")


@router.message(Subject.drive_link)
async def set_subject_drive_link(message: Message, state: FSMContext) -> None:
    await state.update_data(drive_link=message.text)
    subject_data = await state.get_data()
    await state.set_state(Options.option)
    await message.answer(
        f"Your subject:\n"
        f"{hbold('Name')}: {subject_data.get('name')}\n"
        f"{hbold('Description')}: {subject_data.get('description')}\n"
        f"{hbold('Drive link')}: {subject_data.get('drive_link')}"
    )
    return await message.answer(
        "Do you want to create it?", reply_markup=options_keyboard()
    )


@router.message(F.text.casefold() == "yes", Options.option)
async def accept_create(
    message: Message, state: FSMContext, db: Database, teacher: Teacher
) -> None:
    subject_data = await state.get_data()
    await state.clear()
    if await db.create_subject(**subject_data, teacher_id=teacher.id):
        return await message.answer("Subject was created!")
    return await message.answer(
        "Do you want to create it?", reply_markup=options_keyboard()
    )


@router.message(Options.option, F.text.casefold() == "no")
async def decline_create(message: Message, state: FSMContext) -> None:
    await state.clear()
    return await message.answer(
        "Subject was not created. To start again, write /create_subject"
    )


@router.message(Command("my_subjects"))
async def get_subjects(
    message: Message, db: Database, teacher: Teacher
) -> None:
    if subjects := await db.get_subjects_by_teacher_id(teacher.id):
        text = await create_subject_message(subjects)
        await message.answer("Here are your subjects:")
        await message.answer(text)
        return await message.answer(
            "Click on the subject you want to see the details"
        )
    return await message.answer("You don't have any subjects!")
