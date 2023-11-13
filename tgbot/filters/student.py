from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from tgbot.misc.database import Database, Student


class IsStudentFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def __call__(
        self, event: Message | CallbackQuery, db: Database
    ) -> bool | dict[str, Student]:
        if student := await db.get_student(event.from_user.id):
            return {"student": student}
        return False
