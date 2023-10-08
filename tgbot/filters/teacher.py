from aiogram.filters import BaseFilter
from aiogram.types import Message

from tgbot.misc.database import Database, Teacher


class IsTeacherFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def __call__(
        self, message: Message, db: Database
    ) -> bool | dict[str, Teacher]:
        if teacher := await db.get_teacher(message.from_user.id):
            return {"teacher": teacher}
        return False
