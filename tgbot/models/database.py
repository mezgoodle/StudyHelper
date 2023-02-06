from typing import Optional

from sqlalchemy.future.engine import Engine
from sqlmodel import Field, SQLModel, create_engine


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


def create_db_engine(sqlite_file_name: str = "database.db") -> Engine:
    """Function to create sqlmodel engine

    Args:
        sqlite_file_name (str, optional): Path to the database. Defaults to "database.db".

    Returns:
        Engine: engine
    """
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    return create_engine(sqlite_url, echo=True)


def create_db_and_tables(engine: Engine):
    """Funtion to create tables in db with the engine

    Args:
        engine (Engine): engine instance
    """
    SQLModel.metadata.create_all(engine)
