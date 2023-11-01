from json import dumps

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.markdown import hlink

from loader import bot
from tgbot.misc.database import Database
from tgbot.models.models import Subject
from tgbot.states.states import Task


async def create_subject_message(
    subjects: list[Subject],
    methods: list[dict[str, str]],
) -> str:
    rows = []
    for subject in subjects:
        links = []
        for method in methods:
            links.append(
                hlink(
                    method.get("text"),
                    await create_link(subject.id, method.get("name")),
                )
            )
        rows.append(f"{subject.id}. {subject.name}. {', '.join(links)}")

    return "\n".join(rows)


async def create_link(subject_id: int, key: str) -> str:
    return await create_start_link(
        bot, dumps({"key": key, "id": subject_id}), True
    )


async def add_student_to_subject(
    message: Message, payload: dict, db: Database, *args, **kwargs
) -> str:
    if (subject := await db.get_subject(payload.get("id"))) and (
        student := await db.get_student(message.from_user.id)
    ):
        await subject.students.add(student)
        return f'You are now a student of "{subject.name}"'
    return "Subject or student not found"


async def quit_student_to_subject(
    message: Message, payload: dict, db: Database, *args, **kwargs
) -> str:
    if (subject := await db.get_subject(payload.get("id"))) and (
        student := await db.get_student(message.from_user.id)
    ):
        await subject.students.remove(student)
        return f'You are now not a student of "{subject.name}"'
    return "Subject or student not found"


async def add_task(
    message: Message,
    payload: dict,
    db: Database,
    state: FSMContext,
    *args,
    **kwargs,
) -> None:
    if (
        (subject := await db.get_subject(payload.get("id")))
        and (teacher := await subject.teacher)
        and teacher.user_id == message.from_user.id
    ):
        await state.set_state(Task.name)
        await state.update_data(subject_id=subject.id)
        return "Write a name for task"
    return "You are not a teacher of this subject"


utils = {
    "add_subject": add_student_to_subject,
    "quit_subject": quit_student_to_subject,
    "add_task": add_task,
}
