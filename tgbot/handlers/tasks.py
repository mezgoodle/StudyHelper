from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from loader import dp
from tgbot.filters.student import IsStudentFilter
from tgbot.keyboards.inline.callbacks import TaskCallbackFactory
from tgbot.misc.database import Database

router = Router()
router.message.filter(IsStudentFilter())
dp.include_router(router)


@router.callback_query(TaskCallbackFactory.filter(F.action == "create"))
async def create_solution(
    callback: CallbackQuery,
    callback_data: TaskCallbackFactory,
    db: Database,
    state: FSMContext,
) -> Message:
    return await callback.answer("Task created")
