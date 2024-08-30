from datetime import datetime, timezone

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold, hlink

from loader import dp
from tgbot.filters.student import IsStudentFilter
from tgbot.keyboards.inline.callbacks import TaskCallbackFactory
from tgbot.keyboards.inline.solution_keyboard import solution_keyboard
from tgbot.misc.database import Database
from tgbot.misc.storage import Storage
from tgbot.misc.texts import STUDENT_HELP_TEXT
from tgbot.misc.utils import create_subject_message
from tgbot.models.models import Student

router = Router()
router.message.filter(IsStudentFilter())
router.callback_query.filter(IsStudentFilter())
dp.include_router(router)


@router.message(Command("is_student"))
async def check_student(message: Message) -> Message:
    await message.answer("You are a student!")
    return await message.answer(STUDENT_HELP_TEXT)


@router.message(Command("my_subjects"))
async def get_subjects(
    message: Message, db: Database, student: Student
) -> None:
    if subjects := await db.get_student_subjects(student):
        text = await create_subject_message(
            subjects,
            [
                {"text": "Quit from subject", "name": "quit_subject"},
                {"text": "See tasks", "name": "see_tasks"},
            ],
        )
        await message.answer("Here are your subjects:")
        return await message.answer(text)
    return await message.answer("You don't have any subjects!")


@router.message(Command("upcoming_tasks"))
async def show_upcoming_tasks(
    message: Message, db: Database, student: Student
) -> None:
    subjects = await db.get_student_subjects(student)
    for subject in subjects:
        subject_text = f"Your tasks for {hbold(subject.name)}:"
        tasks = await subject.tasks.all().order_by("due_date")
        if tasks:
            tasks_texts = []
            today = datetime.now(timezone.utc)
            for task in (
                await subject.tasks.all()
                .order_by("due_date")
                .filter(due_date__gte=today)
            ):
                solution = await db.solution.filter(
                    student_id=student.pk, subject_task_id=task.pk
                ).first()
                is_done = "✅" if solution else "❌"
                text = f"* Name: {hbold(task.name)}. Due date: {hbold(task.due_date.strftime('%d/%m/%Y'))}. Is done: {is_done}"
                if solution:
                    text += f" Your grade: {hbold(solution.grade)}"
                tasks_texts.append(text)
            tasks_text = "\n".join(tasks_texts)
            await message.answer(subject_text + "\n" + tasks_text)
        else:
            await message.answer(
                subject_text + "\nThere are no tasks for this subject."
            )
    return None


@router.callback_query(TaskCallbackFactory.filter(F.action == "see"))
async def see_my_solution(
    callback: CallbackQuery,
    callback_data: TaskCallbackFactory,
    db: Database,
    storage: Storage,
) -> Message:
    if solution := await db.get_student_solution(
        callback.from_user.id, callback_data.task_id
    ):
        text = "\n".join(
            [
                f"{hbold('Student')}: {solution.student.name}",
                f"{hbold('Grade')}: {solution.grade}",
                f"{hbold('File link')}: {hlink('Click here', storage.create_presigned_url(solution.file_link))}",
            ]
        )
        await callback.message.answer(
            text,
            reply_markup=solution_keyboard(solution.id, solution.grade),
        )
    else:
        await callback.message.answer("There is no solution.")
    return await callback.answer()
