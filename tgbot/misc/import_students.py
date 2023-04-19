from pathlib import Path

from aiogram.types import Message
from aiogram.utils.markdown import hbold
from pandas import read_csv

from tgbot.misc.consts import FILE_EXTENSIONS
from tgbot.models.database import Database
from tgbot.models.validation_models import ValidationModel


async def parse_students_from_file(path: Path, db: Database, message: Message) -> int:
    extension = path.suffix
    df = FILE_EXTENSIONS.get(extension, read_csv)(path)
    df_dict = df.to_dict(orient="records")
    ValidationModel(dataframe=df_dict)
    number_of_students = len(df_dict)
    for index, student in enumerate(df_dict):
        try:
            _ = db.create_student(
                name=student["name"],
                username=student["username"],
                group=student["group"],
                telegram_id=student["telegram_id"],
                subject_name=student["subjects"],
            )
        except Exception as e:
            await message.answer(f"Row {index} was not added. Error: {hbold(e)}")
            number_of_students -= 1
    return number_of_students
