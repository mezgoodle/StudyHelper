from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from tgbot.models.database import Database


class IsTeacherFilter(BoundFilter):
    key = "is_teacher"

    def __init__(self, is_teacher):
        self.is_teacher = is_teacher

    async def check(self, message: Message):
        db: Database = message.bot.get("db")
        return db.is_teacher(message.from_user.id)
