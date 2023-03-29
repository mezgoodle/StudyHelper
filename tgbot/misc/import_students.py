from pathlib import Path

from pandas import read_csv, read_excel

FILE_EXTENSIONS = {
    ".csv": read_csv,
    ".xlsx": read_excel,
    ".xls": read_excel,
}


def parse_students_from_file(path: Path):
    extension = path.suffix
    df = FILE_EXTENSIONS.get(extension, read_csv)(path)
    print(df)
