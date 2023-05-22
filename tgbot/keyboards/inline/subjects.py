from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.keyboards.inline.callback_data import subject_callback
from tgbot.models.database import Subject


def markup(subject: list[Subject]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for subject in subject:
        markup.row(
            InlineKeyboardButton(
                text=subject.name,
                callback_data=subject_callback.new("show", subject.id),
            ),
            InlineKeyboardButton(
                text="Delete from me",
                callback_data=subject_callback.new("delete", subject.id),
            ),
            InlineKeyboardButton(
                text="Edit this subject",
                callback_data=subject_callback.new("edit", subject.id),
            ),
        )
    return markup
