from aiogram.filters import BaseFilter
from aiogram.types import Message

from tgbot.misc.database import Database, Student


class IsStudentFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def __call__(
        self, message: Message, db: Database
    ) -> bool | dict[str, Student]:
        if student := await db.get_student(message.from_user.id):
            return {"student": student}
        return False
