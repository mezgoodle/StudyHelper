from typing import Optional

from sqlalchemy.future.engine import Engine
from sqlmodel import Field, Session, SQLModel, create_engine


class Database:
    def __init__(self, sqlite_file_name: str = "database.db"):
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = create_engine(sqlite_url, echo=True)
        self.session = Session(self.engine)
        SQLModel.metadata.create_all(self.engine)


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
