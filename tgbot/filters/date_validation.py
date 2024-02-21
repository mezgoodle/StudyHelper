from datetime import date, datetime

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message


class IsValidDateFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def __call__(
        self, event: Message | CallbackQuery
    ) -> bool | dict[str, str]:
        try:
            if (
                validated_date := datetime.strptime(
                    event.text, "%d/%m/%Y"
                ).date()
            ) and validated_date >= date.today():
                return {"validated_date": validated_date.isoformat()}
            return False
        except ValueError:
            return False
