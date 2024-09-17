from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from loader import bot, dp
from tgbot.keyboards.inline.callbacks import SupportCallbackFactory
from tgbot.keyboards.inline.support_keyboard import support_keyboard
from tgbot.states.states import Communication

router = Router()
dp.include_router(router)


@router.callback_query(SupportCallbackFactory.filter(F.messages == "one"))
async def send_to_teacher(
    callback: CallbackQuery,
    callback_data: SupportCallbackFactory,
    state: FSMContext,
) -> None:
    user_id = callback_data.user_id
    await state.set_state(Communication.wait_for_message)
    await state.update_data({"second_id": user_id})
    return await callback.message.answer("Write your message")


@router.message(Communication.wait_for_message)
async def write_message(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    second_id = data.get("second_id")
    await bot.send_message(
        second_id, "You have a new message. Answer by clicking on it."
    )
    keyboard = await support_keyboard(
        messages="one", user_id=message.from_user.id
    )
    await message.copy_to(second_id, reply_markup=keyboard)
    await state.clear()
    return await message.answer("Your message has been sent")
