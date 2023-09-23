from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.misc.database import Database

router = Router()
dp.include_router(router)


@router.message(Command("teams"))
async def get_teams_handler(message: Message, db: Database) -> None:
    teams = await db.get_teams()
    print(teams)
    return await message.answer("Teams are printed")


@router.message(Command("create_team"))
async def create_team_handler(message: Message, db: Database) -> None:
    team_name = "test_team"
    created_team = await db.create_team(team_name)
    return await message.answer(f"Team {created_team} created")
