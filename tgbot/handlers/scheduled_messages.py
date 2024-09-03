from datetime import datetime, timezone

from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from tgbot.misc.database import Database


async def scheduled_notification(bot: Bot, db: Database) -> Message:
    students = await db.get_students()

    for student in students:
        header = "Your upcoming tasks:\n\n"
        await bot.send_message(chat_id=student.user_id, text=header)
        subjects = await student.subjects.all()
        for subject in subjects:

            tasks = (
                await subject.tasks.all()
                .order_by("due_date")
                .filter(due_date__gte=datetime.now(timezone.utc))
            )
            task_text = (
                "\n".join(
                    f"{task.name}. Due date: {task.due_date.strftime('%d/%m/%Y')}"
                    for task in tasks
                )
                or "No upcoming tasks"
            )
            await bot.send_message(
                chat_id=student.user_id,
                text=f"Tasks for subject {hbold(subject.name)}:\n" + task_text,
            )
    return
