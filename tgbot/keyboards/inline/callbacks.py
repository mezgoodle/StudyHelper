from aiogram.filters.callback_data import CallbackData


class TaskCallbackFactory(CallbackData, prefix="task"):
    subject_id: int
    task_id: int
    action: str | None
