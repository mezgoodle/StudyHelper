from aiogram.fsm.state import State, StatesGroup


class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()


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
