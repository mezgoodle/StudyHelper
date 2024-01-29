from aiogram.fsm.state import State, StatesGroup


class Subject(StatesGroup):
    name = State()
    description = State()


class Options(StatesGroup):
    option = State()


class Task(StatesGroup):
    name = State()
    description = State()
    due_date = State()


class Solution(StatesGroup):
    task_id = State()
    student_id = State()
    file_link = State()
