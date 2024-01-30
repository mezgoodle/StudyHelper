from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Show help"),
        BotCommand(command="cancel", description="Cancel current state"),
        BotCommand(
            command="register_student", description="Register as student"
        ),
        BotCommand(
            command="register_teacher", description="Register as teacher"
        ),
    ]
    await bot.set_my_commands(commands=commands)
