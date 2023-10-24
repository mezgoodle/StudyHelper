from json import dumps

from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.markdown import hlink

from loader import bot
from tgbot.misc.database import Database
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


async def add_student_to_subject(
    message: Message, payload: dict, db: Database
) -> str:
    if (subject := await db.get_subject(payload.get("id"))) and (
        student := await db.get_student(message.from_user.id)
    ):
        await subject.students.add(student)
        return f'You are now a student of "{subject.name}"'
    return "Subject or student not found"


utils = {
    "add_subject": add_student_to_subject,
}
