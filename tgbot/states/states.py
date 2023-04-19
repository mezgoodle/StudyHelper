from aiogram.dispatcher.filters.state import State, StatesGroup


class Student(StatesGroup):
    group = State()
    subject = State()
