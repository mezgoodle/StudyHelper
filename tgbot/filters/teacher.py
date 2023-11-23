from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from tgbot.misc.database import Database, Teacher


class IsTeacherFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def __call__(
        self, event: Message | CallbackQuery, db: Database
    ) -> bool | dict[str, Teacher]:
        if teacher := await db.get_teacher(event.from_user.id):
            return {"teacher": teacher}
        return False
