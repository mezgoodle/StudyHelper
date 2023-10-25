from json import dumps

from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.markdown import hlink

from loader import bot
from tgbot.misc.database import Database
from tgbot.models.models import Subject


async def create_subject_message(subjects: list[Subject]) -> str:
    """Makes a message with a list of subjects and links to act on them.

    Parameters
    ----------
    subjects : list[Subject]
        List of subjects

    Returns
    -------
    str
        Message with a list of subjects and links to act on them.
    """
    rows = []
    for subject in subjects:
        link = await create_link(subject.id)
        rows.append(
            f"{subject.id}. {subject.name}. {hlink('Invite students',link)}"
        )

    return "\n".join(rows)


async def create_link(subject_id: int, key: str = "add_subject") -> str:
    """Creates a link to act on a subject

    Parameters
    ----------
    subject_id : int
        ID of the subject

    Returns
    -------
    str
        Link to act on a subject with dumped data
    """
    return await create_start_link(
        bot, dumps({"key": key, "id": subject_id}), True
    )


async def add_student_to_subject(
    message: Message, payload: dict, db: Database
) -> str:
    """Adds a student to a subject

    Parameters
    ----------
    message : Message
        Telegram message
    payload : dict
        Payload from the deep link
    db : Database
        instance of Database

    Returns
    -------
    str
        Result message
    """
    if (subject := await db.get_subject(payload.get("id"))) and (
        student := await db.get_student(message.from_user.id)
    ):
        await subject.students.add(student)
        return f'You are now a student of "{subject.name}"'
    return "Subject or student not found"


utils = {
    "add_subject": add_student_to_subject,
}
