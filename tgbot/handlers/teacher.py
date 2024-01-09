from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from loader import dp
from tgbot.filters.teacher import IsTeacherFilter
from tgbot.keyboards.inline.callbacks import (
    SolutionCallbackFactory,
    TaskCallbackFactory,
)
from tgbot.keyboards.inline.solution_keyboard import solution_keyboard
from tgbot.keyboards.reply.options_keyboard import options_keyboard
from tgbot.misc.database import Database
from tgbot.misc.texts import TEACHER_HELP_TEXT
from tgbot.misc.utils import create_subject_message
from tgbot.models.models import Solution, Teacher
from tgbot.states.states import Options, Subject, Task

router = Router()
router.message.filter(IsTeacherFilter())
router.callback_query.filter(IsTeacherFilter())
dp.include_router(router)


@router.message(Command("is_teacher"))
async def check_teacher(message: Message) -> Message:
    await message.answer("You are a teacher!")
    return await message.answer(TEACHER_HELP_TEXT, parse_mode="HTML")


@router.message(Command("create_subject"))
async def create_subject(message: Message, state: FSMContext) -> None:
    await state.set_state(Subject.name)
    return await message.answer("Write a name for subject name")


@router.message(Subject.name)
async def set_subject_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Subject.description)
    return await message.answer("Write a description for subject")


@router.message(Subject.description)
async def set_subject_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(Subject.drive_link)
    return await message.answer("Write a google drive link")


@router.message(Subject.drive_link)
async def set_subject_drive_link(
    message: Message, state: FSMContext, db: Database, teacher: Teacher
) -> None:
    await state.update_data(drive_link=message.text)
    subject_data = await state.get_data()
    await state.set_state(Options.option)
    await state.update_data(
        {"method": db.create_subject, "teacher_id": teacher.id}
    )
    await message.answer(
        f"Your subject:\n"
        f"{hbold('Name')}: {subject_data.get('name')}\n"
        f"{hbold('Description')}: {subject_data.get('description')}\n"
        f"{hbold('Drive link')}: {subject_data.get('drive_link')}"
    )
    return await message.answer(
        "Do you want to create it?", reply_markup=options_keyboard()
    )


@router.message(F.text.casefold() == "yes", Options.option)
async def accept_create(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    db_method = data.pop("method")
    await state.clear()
    if await db_method(**data):
        return await message.answer("Object was created!")
    return await message.answer("Object was not created. Try again.")


@router.message(Options.option, F.text.casefold() == "no")
async def decline_create(message: Message, state: FSMContext) -> None:
    await state.clear()
    return await message.answer("Object was not created. Try again.")


@router.message(Task.name)
async def set_task_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Task.description)
    return await message.answer("Write a description for subject")


@router.message(Task.description)
async def set_task_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(Task.due_date)
    return await message.answer(
        "Please, write a due date in format dd/mm/yyyy"
    )


@router.message(Task.due_date)
async def set_task_due_date(
    message: Message, state: FSMContext, db: Database
) -> None:
    await state.update_data(
        due_date=datetime.strptime(message.text, "%d/%m/%Y")
    )
    task_data = await state.get_data()
    await state.set_state(Options.option)
    await state.update_data({"method": db.create_subject_task})
    await message.answer(
        f"Your task:\n"
        f"{hbold('Name')}: {task_data.get('name')}\n"
        f"{hbold('Description')}: {task_data.get('description')}\n"
        f"{hbold('Due date')}: {task_data.get('due_date')}"
    )
    return await message.answer(
        "Do you want to create it?", reply_markup=options_keyboard()
    )


@router.message(Command("my_subjects"))
async def get_subjects(
    message: Message, db: Database, teacher: Teacher
) -> None:
    if subjects := await db.get_subjects_by_teacher_id(teacher.id):
        text = await create_subject_message(
            subjects,
            [
                {"text": "Invite students", "name": "add_subject"},
                {"text": "Add task", "name": "add_task"},
                {"text": "See tasks", "name": "see_tasks"},
            ],
        )
        await message.answer("Here are your subjects:")
        await message.answer(text)
        return await message.answer("Click on the subject actions")
    return await message.answer("You don't have any subjects!")


@router.callback_query(
    TaskCallbackFactory.filter(F.action == "show_solutions")
)
async def show_solutions_for_task(
    callback: CallbackQuery,
    callback_data: TaskCallbackFactory,
    db: Database,
) -> Message:
    solutions: list[Solution] = await db.get_solutions_for_task(
        callback_data.task_id
    )
    if not solutions:
        await callback.message.answer("There are no solutions.")
    else:
        for solution in solutions:
            text = "\n".join(
                [
                    f"{hbold('Student')}: {solution.student.name}",
                    f"{hbold('Grade')}: {solution.grade}",
                    f"{hbold('File link')}: {solution.file_link}",
                ]
            )
            await callback.message.answer(
                text,
                reply_markup=solution_keyboard(solution.id, solution.grade),
            )
    return await callback.answer()


@router.callback_query(SolutionCallbackFactory.filter())
async def review_solution(
    callback: CallbackQuery,
    callback_data: SolutionCallbackFactory,
    db: Database,
) -> Message:
    if new_solution := await db.update_solution_grade(
        callback_data.solution_id,
        callback_data.grade,
    ):
        text = "\n".join(
            [
                f"{hbold('Student')}: {new_solution.student.name}",
                f"{hbold('Grade')}: {new_solution.grade}",
                f"{hbold('File link')}: {new_solution.file_link}",
            ]
        )
        await callback.message.edit_text(
            text,
            reply_markup=solution_keyboard(
                new_solution.id, new_solution.grade
            ),
        )
        return await callback.answer("Solution was reviewed")
    return await callback.answer("Error was occurred")
