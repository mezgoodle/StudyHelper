from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callbacks import TaskCallbackFactory
from tgbot.misc.database import Database

TASK_BUTTONS = [
    {"text": "Create a solution", "action_text": "create"},
    {"text": "See my solution", "action_text": "see"},
    {"text": "Not graded"},
]


async def task_keyboard(
    subject_id: int, task_id: int, user_id: int, db: Database
) -> InlineKeyboardMarkup:
    buttons_list = TASK_BUTTONS
    if solution := await db.get_student_solution(user_id, task_id):
        buttons_list[2]["text"] = f"Your grade: {solution.grade}"
    if await db.is_teacher(user_id):
        buttons_list = [
            {"text": "See solutions", "action_text": "show_solutions"},
        ]
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        *[
            InlineKeyboardButton(
                text=item.get("text"),
                callback_data=TaskCallbackFactory(
                    subject_id=subject_id,
                    task_id=task_id,
                    action=item.get("action_text"),
                ).pack(),
            )
            for item in buttons_list
        ]
    )
    return keyboard.as_markup()
