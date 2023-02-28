from typing import Optional, Union

from loguru import logger
from sqlalchemy.exc import CompileError, MultipleResultsFound
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class SubjectStudentLink(SQLModel, table=True):
    subject: Optional[int] = Field(
        default=None, foreign_key="subject.id", primary_key=True
    )
    student: Optional[int] = Field(
        default=None, foreign_key="student.id", primary_key=True
    )


class SubjectTeacherLink(SQLModel, table=True):
    subject: Optional[int] = Field(
        default=None, foreign_key="subject.id", primary_key=True
    )
    teacher: Optional[int] = Field(
        default=None, foreign_key="teacher.id", primary_key=True
    )


class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    students: list["Student"] = Relationship(
        back_populates="subjects", link_model=SubjectStudentLink
    )
    teacher: Optional["Teacher"] = Relationship(
        back_populates="subjects", link_model=SubjectTeacherLink
    )


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    telegram_id: int = Field(index=True)
    group: str
    username: str
    subjects: list[Subject] = Relationship(
        back_populates="students", link_model=SubjectStudentLink
    )


class Teacher(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    username: str
    telegram_id: int = Field(index=True)
    subjects: list[Subject] = Relationship(
        back_populates="teacher", link_model=SubjectTeacherLink
    )


class Database:
    def __init__(self, sqlite_file_name: str = "database.db"):
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = create_engine(sqlite_url, echo=True)
        SQLModel.metadata.create_all(self.engine)

    def create_teacher(
        self, name: str, telegram_id: int, username: str
    ) -> Optional[Teacher]:
        """Method for creating a teacher

        Args:
            name (str): full-name of the teacher
            telegram_id (int): telegram id of the teacher
            username (str): username of the teacher

        Returns:
            Optional[Teacher]: created object
        """
        teacher = Teacher(name=name, telegram_id=telegram_id, username=username)
        return self.__create(teacher)

    def get_teacher(self, telegram_id: int) -> Optional[Teacher]:
        """Method for getting a teacher by telegram id

        Args:
            telegram_id (int): telegram id of the teacher

        Returns:
            Optional[Teacher]: teacher object
        """
        with Session(self.engine) as session:
            teacher = session.exec(
                select(Teacher).where(Teacher.telegram_id == telegram_id)
            ).first()
            return teacher

    def is_teacher(self, telegram_id: int) -> bool:
        """Method for checking if a user is a teacher

        Args:
            telegram_id (int): telegram id of the user

        Returns:
            bool: True if user is a teacher, False otherwise
        """
        return self.get_teacher(telegram_id) is not None

    def __create(
        self, obj: Union[Teacher, Student, Subject]
    ) -> Optional[Union[Teacher, Student, Subject]]:
        """Private method for creating an object

        Args:
            obj (Union[Teacher, Student, Subject]): object to create

        Returns:
            Optional[Union[Teacher, Student, Subject]]: created object
        """
        logger.info("Try to create an object")
        with Session(self.engine) as session:
            try:
                session.add(obj)
                session.commit()
                session.refresh(obj)
                logger.info("Successfull creation")
                return obj
            except CompileError as e:
                logger.error(f"Error: {e}")
