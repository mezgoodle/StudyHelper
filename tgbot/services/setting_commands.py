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
        BotCommand(
            command="is_teacher", description="Check if you are a teacher"
        ),
        BotCommand(
            command="is_student", description="Check if you are a student"
        ),
    ]
    await bot.set_my_commands(commands=commands)
