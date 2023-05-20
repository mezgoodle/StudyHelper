from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.keyboards.reply.subjects import create_markup
from tgbot.models.database import Database
from tgbot.states.states import Student


@dp.message_handler(Command(["register_student"]))
async def register_student(message: Message) -> Message:
    await Student.first()
    return await message.answer("Send your group")


@dp.message_handler(state=Student.group)
async def process_group(message: Message, state: FSMContext) -> Message:
    db: Database = message.bot.get("db")
    try:
        subjects = db.get_subjects_by_group(message.text)
    except ValueError:
        await state.finish()
        return await message.answer("Group is not founded")
    except Exception:
        await state.finish()
        return await message.answer("Something went wrong")
    if not subjects:
        await state.finish()
        return await message.answer("Subjects are not founded")
    keyboard = create_markup(subjects)
    await state.update_data(group=message.text)
    await Student.next()
    return await message.answer("Choose your subject", reply_markup=keyboard)


@dp.message_handler(state=Student.subject)
async def process_subject(message: Message, state: FSMContext) -> Message:
    data = await state.get_data()
    await state.finish()
    db: Database = message.bot.get("db")
    user = message.from_user
    if db.get_student(user.id, data["group"]):
        return await message.answer(
            "You are already registered as student for this subject"
        )

    if db.create_student(
        name=user.full_name,
        telegram_id=user.id,
        username=user.username,
        group_name=data["group"],
        subject_name=message.text,
    ):
        return await message.answer(
            "You are registered as student for this subject"
        )
    return await message.answer("Something went wrong")
