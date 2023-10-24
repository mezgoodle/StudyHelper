from json import dumps

from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.markdown import hlink

from loader import bot
from tgbot.models.models import Subject


async def create_subject_message(subjects: list[Subject]) -> str:
    rows = []
    for subject in subjects:
        link = await create_link(subject)
        rows.append(
            f"{subject.id}. {subject.name}. {hlink('Invite students',link)}"
        )

    return "\n".join(rows)


async def create_link(subject: Subject) -> str:
    return await create_start_link(
        bot, dumps({"key": "add_subject", "id": subject.id}), True
    )
