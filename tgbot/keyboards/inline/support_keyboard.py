from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callbacks import SupportCallbackFactory


async def support_keyboard(
    teacher_id: int | None = None, user_id: int | None = None
) -> InlineKeyboardMarkup:
    if user_id:
        contact_id = user_id
        text = "Answer to student"
    else:
        contact_id = teacher_id
        text = "Write your message"
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=text,
            callback_data=SupportCallbackFactory(user_id=contact_id).pack(),
        )
    )
    return keyboard.as_markup()
