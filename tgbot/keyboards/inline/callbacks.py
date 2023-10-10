from aiogram.filters.callback_data import CallbackData


class SubjectCallback(CallbackData, prefix="subject"):
    subject_id: int
