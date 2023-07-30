from typing import List, NewType, Optional, Tuple, Union

from loguru import logger
from sqlalchemy.exc import CompileError
from sqlmodel import (
    Field,
    Relationship,
    Session,
    SQLModel,
    create_engine,
    select,
)


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


class GroupSubjectLink(SQLModel, table=True):
    group: Optional[int] = Field(
        default=None, foreign_key="group.id", primary_key=True
    )
    subject: Optional[int] = Field(
        default=None, foreign_key="subject.id", primary_key=True
    )


class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    subjects: list["Subject"] = Relationship(
        back_populates="groups", link_model=GroupSubjectLink
    )
    students: list["Student"] = Relationship(back_populates="group")


class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    students: list["Student"] = Relationship(
        back_populates="subjects", link_model=SubjectStudentLink
    )
    teacher: Optional["Teacher"] = Relationship(
        back_populates="subjects", link_model=SubjectTeacherLink
    )
    groups: list["Group"] = Relationship(
        back_populates="subjects", link_model=GroupSubjectLink
    )


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    telegram_id: int = Field(index=True)
    username: str
    subjects: list[Subject] = Relationship(
        back_populates="students", link_model=SubjectStudentLink
    )
    group_id: Optional[int] = Field(default=None, foreign_key="group.id")
    group: Optional[Group] = Relationship(back_populates="students")


class Teacher(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    username: str
    telegram_id: int = Field(index=True)
    subjects: list[Subject] = Relationship(
        back_populates="teacher", link_model=SubjectTeacherLink
    )


LIST_OF_OBJECTS_TYPE = NewType(
    "LIST_OF_OBJECTS", List[Union[Subject, Student, Teacher, Group]]
)


class Database:
    def __init__(self, sqlite_file_name: str = "database.db"):
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = create_engine(sqlite_url, echo=True)
        SQLModel.metadata.create_all(self.engine)

    def create(
        self, obj: Union[Teacher, Student, Subject, Group]
    ) -> Optional[Union[Teacher, Student, Subject, Group]]:
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

    def update(
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

    def get(
        self,
        objects: LIST_OF_OBJECTS_TYPE,
        conditions: tuple = None,
    ) -> Optional[LIST_OF_OBJECTS_TYPE]:
        logger.info("Try to get an object")
        logger.info(f"{objects=}")
        logger.info(f"{conditions=}")
        with Session(self.engine) as session:
            try:
                if conditions is None:
                    results = session.exec(select(*objects)).all()
                else:
                    results = session.exec(
                        select(*objects).where(*conditions)
                    ).all()
                logger.success("Successfull get")
                logger.info(f"{results=}")
                return results
            except CompileError as e:
                logger.error(f"Error: {e}")

    def drop_database(self):
        SQLModel.metadata.drop_all(self.engine)


class TeacherDB(Database):
    def is_teacher(self, telegram_id: int) -> bool:
        return self.get_teacher(telegram_id) is not None

    def get_teacher(self, telegram_id: int) -> Optional[Teacher]:
        try:
            return self.get(
                [Teacher], conditions=(Teacher.telegram_id == telegram_id,)
            )[0]
        except IndexError:
            return None

    def get_teachers(self) -> Optional[list[Teacher]]:
        return self.get([Teacher])

    def create_teacher(
        self, name: str, telegram_id: int, username: str
    ) -> Optional[Teacher]:
        teacher = Teacher(
            name=name, telegram_id=telegram_id, username=username
        )
        return self.create(teacher)


class GroupDB(Database):
    def create_group(self, name: str) -> Optional[Group]:
        group = Group(name=name)
        return self.create(group)

    def get_group(self, name: str) -> Optional[Group]:
        try:
            return self.get([Group], conditions=(Group.name == name,))[0]
        except IndexError:
            return None

    def get_groups(self) -> Optional[list[Group]]:
        return self.get([Group])


class SubjectDB(Database):
    def __init__(self):
        self.group_db = GroupDB()
        self.teacher_db = TeacherDB()
        super().__init__()

    def create_subject(
        self, name: str, teacher_telegram_id: int, group_name: str
    ) -> Optional[Subject]:
        teacher = self.teacher_db.get_teacher(teacher_telegram_id)
        if group := self.group_db.get_group(group_name):
            subject = Subject(name=name, teacher=[teacher], groups=[group])
            return self.create(subject)
        group = self.group_db.create_group(group_name)
        subject = Subject(name=name, teacher=[teacher], groups=[group])
        return self.create(subject)

    def get_subject(self, name: str) -> Optional[Subject]:
        try:
            return self.get(
                [Subject, Group], conditions=(Subject.name == name,)
            )[0]
        except IndexError:
            return None

    def get_subjects(self) -> Optional[list[Subject]]:
        return self.get([Subject])

    def get_subjects_by_group(
        self, group_name: str
    ) -> Optional[list[Subject]]:
        if group := self.group_db.get_group(group_name):
            return [
                data[1]
                for data in self.get(
                    [Group, Subject], conditions=(Group.id == group.id,)
                )
            ]
        raise ValueError("Group is not founded")

    def get_subjects_by_teacher(
        self, teacher_telegram_id: int
    ) -> Optional[list[Subject]]:
        if teacher := self.teacher_db.get_teacher(teacher_telegram_id):
            return [
                data[1]
                for data in self.get(
                    [Teacher, Subject], conditions=(Teacher.id == teacher.id,)
                )
            ]
        raise ValueError("Teacher is not founded")


class StudentDB(Database):
    def __init__(self):
        self.group_db = GroupDB()
        self.subject_db = SubjectDB()
        super().__init__()

    def is_student(self, telegram_id: int, group_name: str) -> bool:
        return self.get_student(telegram_id, group_name) is not None

    def get_student(
        self, telegram_id: int, group_name: str
    ) -> Optional[Tuple[Student, Subject, Group]]:
        if group := self.group_db.get_group(group_name):
            try:
                return self.get(
                    [Student, Subject, Group],
                    conditions=(
                        Student.telegram_id == telegram_id,
                        Student.group_id == group.id,
                    ),
                )[0]
            except IndexError:
                return None
        raise ValueError("Group is not founded")

    def get_students(self) -> Optional[list[Tuple[Student, Subject]]]:
        return self.get([Student, Subject])

    def create_student(
        self,
        name: str,
        telegram_id: int,
        group_name: str,
        username: str,
        subject_name: str,
    ) -> Optional[Student]:
        if subject_info := self.subject_db.get_subject(subject_name):
            if student_info := self.get_student(telegram_id, group_name):
                student: Student = student_info[0]
                student.subjects.append(subject_info[0])
                return self.update(student)
            if group := self.group_db.get_group(group_name):
                student = Student(
                    name=name,
                    telegram_id=telegram_id,
                    group_id=group.id,
                    username=username,
                    subjects=[subject_info[0]],
                )
                return self.create(student)
            raise ValueError("Group is not created")
        raise ValueError("Subject is not created")
