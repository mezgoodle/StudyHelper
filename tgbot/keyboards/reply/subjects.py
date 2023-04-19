from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from tgbot.models.database import Subject


def create_markup(subjects: list[Subject]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for subject in subjects:
        markup.add(KeyboardButton(subject.name))
    return markup
