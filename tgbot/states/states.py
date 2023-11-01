from aiogram.fsm.state import State, StatesGroup


class Subject(StatesGroup):
    name = State()
    description = State()
    drive_link = State()


class Options(StatesGroup):
    option = State()


class Task(StatesGroup):
    name = State()
    description = State()
    due_date = State()
