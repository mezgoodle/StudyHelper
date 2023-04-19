from typing import Optional, Union

from loguru import logger
from sqlalchemy.exc import CompileError
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
        teacher = Teacher(name=name, telegram_id=telegram_id, username=username)
        return self.__create(teacher)

    def create_student(
        self, name: str, telegram_id: int, group: str, username: str, subject_name: str
    ) -> Optional[Student]:
        if student := self.get_student(telegram_id):
            student.subjects.append(subject_name)
            return self.__update(student)
        if subject := self.get_subject(subject_name):
            student = Student(
                name=name,
                telegram_id=telegram_id,
                group=group,
                username=username,
                subjects=[subject],
            )
            return self.__create(student)

    def create_subject(self, name: str, teacher_telegram_id: int) -> Optional[Subject]:
        teacher = self.get_teacher(teacher_telegram_id)
        subject = Subject(name=name, teacher=[teacher])
        return self.__create(subject)

    def get_teacher(self, telegram_id: int) -> Optional[Teacher]:
        return self.__get(Teacher, condition=(Teacher.telegram_id, telegram_id))

    def get_teachers(self) -> list[Teacher]:
        return self.__get(Teacher)

    def get_student(self, telegram_id: int) -> Optional[Student]:
        return self.__get(Student, condition=(Student.telegram_id, telegram_id))

    def get_students(self) -> list[Student]:
        return self.__get(Student)

    def get_subject(self, name: str) -> Optional[Subject]:
        return self.__get(Subject, condition=(Subject.name, name))

    def get_subjects(self) -> list[Subject]:
        return self.__get(Subject)

    def is_teacher(self, telegram_id: int) -> bool:
        return self.get_teacher(telegram_id) is not None

    def is_student(self, telegram_id: int) -> bool:
        return self.get_student(telegram_id) is not None

    def __create(
        self, obj: Union[Teacher, Student, Subject]
    ) -> Optional[Union[Teacher, Student, Subject]]:
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

    def __update(
        self, obj: Union[Teacher, Student, Subject]
    ) -> Optional[Union[Teacher, Student, Subject]]:
        with Session(self.engine) as session:
            try:
                session.add(obj)
                session.commit()
                session.refresh(obj)
                return obj
            except CompileError as e:
                logger.error(f"Error: {e}")

    def __get(
        self, obj: Union[Teacher, Student, Subject], condition: tuple = None
    ) -> Optional[Union[Teacher, Student, Subject]]:
        logger.info("Try to get an object")
        with Session(self.engine) as session:
            try:
                if condition is None:
                    results = session.exec(select(obj))
                else:
                    results = session.exec(
                        select(obj).where(condition[0] == condition[1])
                    ).first()
                logger.info("Successfull get")
                return results
            except CompileError as e:
                logger.error(f"Error: {e}")
