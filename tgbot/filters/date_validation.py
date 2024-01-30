from datetime import date, datetime

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from tgbot.misc.database import Database


class IsValidDataFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def __call__(
        self, event: Message | CallbackQuery, db: Database
    ) -> bool | dict[str, date]:
        try:
            if (
                validated_date := datetime.strptime(
                    event.text, "%d/%m/%Y"
                ).date()
            ) and validated_date >= date.today():
                return {"validated_date": validated_date}
            return False
        except ValueError:
            return False
