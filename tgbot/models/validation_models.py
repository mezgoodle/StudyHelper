from typing import Optional

from pydantic import BaseModel, Field


class DataframeValidator(BaseModel):
    name: str = Field(...)
    telegram_id: int = Field(...)
    group: str = Field(...)
    username: str = Field(...)
    subjects: str = Field(...)


class ValidationModel(BaseModel):
    dataframe: list[DataframeValidator] = Field(...)
