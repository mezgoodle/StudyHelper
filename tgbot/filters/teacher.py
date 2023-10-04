from aiogram.filters import BaseFilter
from aiogram.types import Message

from tgbot.misc.database import Database


class IsTeacherFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def __call__(self, message: Message, db: Database) -> bool:
        return await db.get_teacher(message.from_user.id) is not None
