from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from loader import dp
from tgbot.filters.student import IsStudentFilter
from tgbot.keyboards.inline.callbacks import TaskCallbackFactory
from tgbot.misc.database import Database
from tgbot.misc.storage import Storage
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
) -> Message:
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
    await bot.download_file(file_path, file_name)
    storage.add_file(file_name, file_link)
    await state.update_data(file_link=file_link)
    data = await state.get_data()
    await state.clear()
    if previous_solution := await db.get_student_solution(
        data.get("student_id"), data.get("subject_task_id")
    ):
        await previous_solution.delete()
    await db.create_solution(**data)
    return await message.answer("Your solution was submitted!")
