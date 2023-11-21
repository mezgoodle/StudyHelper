from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callbacks import SolutionCallbackFactory


def solution_keyboard(
    solution_id: int, current_grade: int
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    buttons_list = []
    for grade in range(1, 6):
        buttons_list.append(
            InlineKeyboardButton(
                text=f"✅{grade}" if grade == current_grade else str(grade),
                callback_data=SolutionCallbackFactory(
                    solution_id=solution_id,
                    grade=grade,
                ).pack(),
            )
        )
    keyboard.row(*buttons_list)
    return keyboard.as_markup()
