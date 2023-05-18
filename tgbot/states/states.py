from aiogram.dispatcher.filters.state import State, StatesGroup


class Student(StatesGroup):
    group = State()
    subject = State()


class Subject(StatesGroup):
    name = State()
    group = State()


class File(StatesGroup):
    file = State()
