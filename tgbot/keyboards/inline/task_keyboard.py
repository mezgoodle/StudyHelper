from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callbacks import TaskCallbackData

TASK_BUTTONS = [
    {"text": "Create a solution", "action_text": "create"},
    {"text": "See my solution", "action_text": "see"},
    {"text": "Done?"},
]


def task_keyboard(subject_id: int, task_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        *[
            InlineKeyboardButton(
                text=item.get("text"),
                callback_data=TaskCallbackData(
                    subject_id=subject_id,
                    task_id=task_id,
                    action=item.get("action_text"),
                ).pack(),
            )
            for item in TASK_BUTTONS
        ]
    )
    return keyboard.as_markup()
