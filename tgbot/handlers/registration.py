from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.keyboards.reply.reg_keyboard import create_markup
from tgbot.models.database import Database


@dp.message_handler(Command(["reg_me"]))
async def reg_me(message: Message, state: FSMContext) -> Message:
    markup = create_markup()
    await state.set_state("choose_role")
    return await message.reply("Оберіть свою роль", reply_markup=markup)


@dp.message_handler(state="choose_role")
async def choose_role(message: Message, state: FSMContext) -> Message:
    if message.text == "Як студента":
        await state.set_state("choose_group")
        return await message.reply("Оберіть свою групу")
    elif message.text == "Як викладача":
        await state.finish()
        db: Database = message.bot.get("db")
        new_teacher = db.create_teacher(
            message.from_user.full_name,
            message.from_user.id,
            message.from_user.username,
        )
        if new_teacher:
            await message.reply("Ви успішно зареєстровані як викладач")
            return await message.answer(
                f"Ваші дані: \nІм'я: {new_teacher.name}\nID: {new_teacher.id}\nUsername: {new_teacher.username}"
            )
        return await message.reply("Сталася помилка, спробуйте ще раз")
