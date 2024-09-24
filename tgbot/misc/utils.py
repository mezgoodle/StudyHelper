import logging
import os
from json import dumps

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.markdown import hbold, hlink

from loader import bot
from tgbot.keyboards.inline.support_keyboard import support_keyboard
from tgbot.keyboards.inline.task_keyboard import task_keyboard
from tgbot.misc.charts import send_chart
from tgbot.misc.database import Database
from tgbot.models.models import Student, Subject, SubjectTask
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
        return await message.answer(
            f'You are now a student of "{subject.name}"'
        )
    return await message.answer("Subject or student not found")


async def quit_student_to_subject(
    message: Message, payload: dict, db: Database, *args, **kwargs
) -> str:
    if (subject := await db.get_subject(payload.get("id"))) and (
        student := await db.get_student(message.from_user.id)
    ):
        await subject.students.remove(student)
        return await message.answer(
            f'You are now not a student of "{subject.name}"'
        )
    return await message.answer("Subject or student not found")


async def see_tasks(
    message: Message,
    payload: dict,
    db: Database,
    *args,
    **kwargs,
) -> str:
    if (subject := await db.get_subject(payload.get("id"))) and (
        tasks := await subject.tasks
    ):
        await message.answer(
            f"Here are your tasks for subject {hbold(subject.name)}"
        )
        for task in tasks:
            await message.answer(
                f"{hbold('Name')}: {task.name}\n"
                f"{hbold('Description')}: {task.description}\n"
                f"{hbold('Due date')}: {task.due_date}",
                reply_markup=await task_keyboard(
                    subject.id, task.id, message.from_user.id, db
                ),
            )
        return await message.answer("Your buttons depend on your role")
    return await message.answer("There are no tasks in this subject")


async def add_task(
    message: Message,
    payload: dict,
    db: Database,
    state: FSMContext,
    *args,
    **kwargs,
) -> str:
    if (
        (subject := await db.get_subject(payload.get("id")))
        and (teacher := await subject.teacher)
        and teacher.user_id == message.from_user.id
    ):
        await state.set_state(Task.name)
        await state.update_data(subject_id=subject.id)
        return await message.answer("Write a name for task")
    return await message.answer("You are not a teacher of this subject")


def delete_file(file_path: str):
    try:
        os.remove(file_path)
        logging.info(f"File {file_path} has been deleted successfully locally")
    except FileNotFoundError:
        logging.error(f"The file {file_path} does not exist")
    except PermissionError:
        logging.error(f"Permission denied: unable to delete {file_path}")
    except OSError as e:
        logging.error(f"Error: {e}")


async def gather_upcoming_tasks(
    db: Database, subject: Subject, tasks: list[SubjectTask], student: Student
) -> str:
    subject_text = f"Your tasks for {hbold(subject.name)}:"
    tasks_texts = []
    for task in tasks:
        solution = await db.solution.filter(
            student_id=student.pk, subject_task_id=task.pk
        ).first()
        is_done = "✅" if solution else "❌"
        text = f"* Name: {hbold(task.name)}. Due date: {hbold(task.due_date.strftime('%d/%m/%Y'))}. Is done: {is_done}"
        if solution:
            text += f" Your grade: {hbold(solution.grade)}"
        tasks_texts.append(text)
    tasks_text = "\n".join(tasks_texts)
    return subject_text + "\n" + tasks_text


async def ask_teacher(
    message: Message, payload: dict, db: Database, *args, **kwargs
) -> str:
    text = "To write a message to the teacher, click a button below:"
    if (subject := await db.get_subject(payload.get("id"))) and (
        teacher := await subject.teacher
    ):
        keyboard = await support_keyboard(teacher_id=teacher.user_id)
        return await message.answer(text, reply_markup=keyboard)
    logging.error("Subject or teacher not found. Can't send message.")
    return await message.answer(
        "Subject or teacher not found. Can't send message."
    )


async def subject_stats(
    message: Message, payload: dict, db: Database, *args, **kwargs
) -> str:
    if subject := await db.get_subject(payload.get("id")):
        subject_stats = await db.get_count_solutions_by_subject(subject)
        stats = {}
        if not subject_stats.values():
            return await message.answer(
                f"Stats for subject {hbold(subject.name)}: No data"
            )
        stats["Tasks names"] = subject_stats.keys()
        stats["Solutions"] = subject_stats.values()
        await message.answer(f"Stats for subject {hbold(subject.name)}:")
        return await send_chart(
            message,
            stats,
            "Tasks names",
            "Solutions",
            "Number of solutions for tasks",
        )


utils = {
    "add_subject": add_student_to_subject,
    "quit_subject": quit_student_to_subject,
    "add_task": add_task,
    "see_tasks": see_tasks,
    "ask_teacher": ask_teacher,
    "subject_stats": subject_stats,
}
