from pathlib import Path

from aiogram.types import Message


def check_extension(
    file_name: str, allowed_extensions: tuple = (".csv", ".xlsx", ".xls")
):
    if not file_name.lower().endswith(allowed_extensions):
        raise Exception(
            """You should send file with students' data.
Formats: <b>.csv</b>, <b>.xlsx</b>, <b>.xls</b>"""
        )


async def download_file(
    file_name: str,
    message: Message,
    folders: tuple[str] = ("files", "imports"),
) -> Path:
    try:
        path_to_download = Path().joinpath(*folders)
        path_to_download.mkdir(parents=True, exist_ok=True)
        path_to_download = path_to_download.joinpath(file_name)
        await message.document.download(destination_file=path_to_download)
        return path_to_download
    except Exception:
        raise Exception("Can't download file")


def delete_file(path: Path):
    if path.exists():
        path.unlink()
