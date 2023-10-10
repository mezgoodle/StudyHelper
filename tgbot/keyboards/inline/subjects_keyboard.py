from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callbacks import SubjectCallback
from tgbot.models.models import Subject


def subject_markup(subjects: list[Subject]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    for subject in subjects:
        markup.button(
            text=subject.name,
            callback_data=SubjectCallback(subject_id=subject.id),
        )
    return markup.as_markup()
