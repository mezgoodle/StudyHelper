from aiogram.types import CallbackQuery, Message

from loader import dp
from tgbot.keyboards.inline.callback_data import subject_callback
from tgbot.models.database import Database


@dp.callback_query_handler(subject_callback.filter(action="show"))
async def deny_offer(call: CallbackQuery, callback_data: dict) -> Message:
    db: Database = call.bot.get("db")
    subjects_and_groups = db.get_subject(callback_data["name"])
    subject = subjects_and_groups[0][0]
    return await call.message.answer(
        f"Name: {subject.name}.\nGroups: {', '.join([group.name for _, group in subjects_and_groups])}"  # noqa: E501
    )
