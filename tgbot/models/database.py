from typing import List, Optional, Union

from loguru import logger
from sqlalchemy.exc import CompileError
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine


class SubjectStudentLink(SQLModel, table=True):
    subject: Optional[int] = Field(
        default=None, foreign_key="subject.id", primary_key=True
    )
    student: Optional[int] = Field(
        default=None, foreign_key="student.id", primary_key=True
    )


class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    students: List["Student"] = Relationship(
        back_populates="subjects", link_model=SubjectStudentLink
    )


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    subjects: List[Subject] = Relationship(
        back_populates="students", link_model=SubjectStudentLink
    )


class Database:
    def __init__(self, sqlite_file_name: str = "database.db"):
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = create_engine(sqlite_url, echo=True)
        SQLModel.metadata.create_all(self.engine)

    # def create_hero(self, name: str, secret_name: str, age: int = None) -> bool:
    #     """Method for creating hero

    #     Args:
    #         name (str): name of the hero
    #         secret_name (str): secret name of the hero
    #         age (int, optional): age of the hero. Defaults to None.

    #     Returns:
    #         bool: status of the operation
    #     """
    #     hero = Hero(name=name, secret_name=secret_name, age=age)
    #     return self.__create(hero)

    # def __create(self, obj: Union[Hero, str]) -> bool:
    #     """Method for creating object in the database

    #     Args:
    #         obj (Union[Hero, str]): instance of the table

    #     Returns:
    #         bool: status of the operation
    #     """
    #     logger.info("Try to create an user")
    #     with Session(self.engine) as session:
    #         try:
    #             session.commit()
    #             logger.info("Successfull creation")
    #         except CompileError as e:
    #             logger.error(f"Error: {e}")
    #             return False
    #     return True
