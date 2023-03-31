from pathlib import Path

from pandas import read_csv, read_excel

from tgbot.models.database import Database
from tgbot.models.validation_models import ValidationModel

FILE_EXTENSIONS = {
    ".csv": read_csv,
    ".xlsx": read_excel,
    ".xls": read_excel,
}


def parse_students_from_file(path: Path, db: Database):
    extension = path.suffix
    df = FILE_EXTENSIONS.get(extension, read_csv)(path)
    df_dict = df.to_dict(orient="records")
    ValidationModel(dataframe=df_dict)
    for student in df_dict:
        create_student(student, db)


def create_student(student: dict, db: Database):
    _ = db.create_student(
        name=student["name"],
        username=student["username"],
        group=student["group"],
        telegram_id=student["telegram_id"],
        subjects=student["subjects"],
    )
