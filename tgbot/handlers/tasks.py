from datetime import date

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold, hlink

from loader import dp
from tgbot.filters.student import IsStudentFilter
from tgbot.keyboards.inline.callbacks import TaskCallbackFactory
from tgbot.misc.database import Database
from tgbot.misc.storage import Storage
from tgbot.misc.utils import delete_file
from tgbot.states.states import Solution

router = Router()
router.message.filter(IsStudentFilter())
router.callback_query.filter(IsStudentFilter())
dp.include_router(router)


@router.callback_query(TaskCallbackFactory.filter(F.action == "create"))
async def create_solution(
    callback: CallbackQuery,
    callback_data: TaskCallbackFactory,
    state: FSMContext,
    db: Database,
) -> Message:
    if subject_task := await db.get_subject_task(callback_data.task_id):
        due_date = subject_task.due_date
        if due_date.date() <= date.today():
            await callback.message.answer(
                "Due date has passed. You can't create solution."
            )
        else:
            await state.set_state(Solution.file_link)
            await state.update_data(
                {
                    "subject_task_id": callback_data.task_id,
                    "student_id": callback.from_user.id,
                }
            )
            await callback.message.answer("Send a file(pdf or docx)")
    return await callback.answer()


@router.message(
    Solution.file_link,
    F.document & F.document.file_name.endswith(".pdf")
    | F.document.file_name.endswith(".docx"),
)
async def set_solution_file_link(
    message: Message,
    state: FSMContext,
    db: Database,
    bot: Bot,
    storage: Storage,
) -> Message:
    file = await bot.get_file(message.document.file_id)
    file_path = file.file_path
    file_name = message.document.file_name
    file_link = f"{message.from_user.username}/{file_name}"
    await state.update_data(file_link=file_link)
    data = await state.get_data()
    task = await db.get_subject_task(data.get("subject_task_id"))
    file_link = f"{task.subject.name}/{file_link}"
    await bot.download_file(file_path, file_name)
    if not storage.add_file(file_name, file_link):
        await message.answer("Error while uploading file")
        return

    await state.clear()
    delete_file(file_name)
    if previous_solution := await db.get_student_solution(
        data.get("student_id"), data.get("subject_task_id")
    ):
        teacher_id = previous_solution.subject_task.subject.teacher.user_id
        objects = storage.get_objects()
        previous_file_link = previous_solution.file_link
        if file_link != previous_file_link and previous_file_link in [
            obj["Key"] for obj in objects
        ]:
            storage.delete_file(previous_file_link)
        if await db.update_solution_file_link(previous_solution, file_link):
            await message.answer("Your solution was updated!")
            return await bot.send_message(
                teacher_id,
                f"Updated solution from @{message.from_user.username} for subject task {hbold(previous_solution.subject_task.name)}. Link {hlink('here', storage.create_presigned_url(file_link))}",
            )
        return await message.answer("Error while updating solution")
    solution = await db.create_solution(**data)
    teacher_id = solution.subject_task.subject.teacher.user_id
    await bot.send_message(
        teacher_id,
        f"New solution from @{message.from_user.username} for subject task {hbold(solution.subject_task.name)}. Link {hlink('here', storage.create_presigned_url(solution.file_link))}",
    )
    return await message.answer("Your solution was submitted!")
