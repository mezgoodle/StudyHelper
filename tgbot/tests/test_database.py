import pytest
from sqlmodel import Session, inspect

from tgbot.models.database import Database, Group, Student, Subject, Teacher


@pytest.fixture(name="db")
def db_fixture():
    return Database()


@pytest.fixture(name="session")
def session_fixture(db: Database):
    with Session(db.engine) as session:
        yield session


@pytest.fixture(name="student")
def student_fixture():
    return {
        "name": "John",
        "telegram_id": 123456789,
        "group_name": "A",
        "username": "john_doe",
        "subject_name": "Math",
    }


@pytest.fixture(name="subject")
def subject_fixture():
    return {"name": "Math", "teacher_telegram_id": 123456789}


@pytest.fixture(name="teacher")
def teacher_fixture():
    return {
        "name": "John",
        "telegram_id": 123456789,
        "username": "john_doe",
    }


class TestDatabase:
    def test_create_student_fail(self, db: Database, student: dict):
        with pytest.raises(ValueError):
            db.create_student(**student)

    def test_create_subject_fail(self, db: Database, subject: dict):
        with pytest.raises(Exception):
            db.create_subject(**subject)

    def test_create_group_fail(self, db: Database):
        with pytest.raises(Exception):
            db.create_group()

    def test_create_teacher_fail(self, db: Database):
        with pytest.raises(Exception):
            db.create_teacher()

    def test_create_teacher(
        self, session: Session, teacher: dict, db: Database
    ):
        db.create_teacher(**teacher)
        db_teacher = session.query(Teacher).filter_by(name="John").first()
        assert db_teacher.name == teacher.get("name")
        assert db_teacher.telegram_id == teacher.get("telegram_id")
        assert db_teacher.username == teacher.get("username")

    def test_create_subject(
        self, session: Session, subject: dict, student: dict, db: Database
    ):
        db.create_subject(**subject, group_name=student.get("group_name"))
        db_subject = session.query(Subject).filter_by(name="Math").first()
        assert db_subject.name == subject.get("name")

    def test_create_student(
        self, session: Session, student: dict, db: Database
    ):
        db.create_student(**student)
        db_student = session.query(Student).filter_by(name="John").first()
        assert db_student.name == student.get("name")
        assert db_student.telegram_id == student.get("telegram_id")
        assert db_student.group.name == student.get("group_name")

    def test_create_group(self, session: Session, db: Database, student: dict):
        db.create_group(student.get("group_name"))
        db_group = session.query(Group).filter_by(name="A").first()
        assert db_group.name == student.get("group_name")

    def test_get_teachers(self, db: Database):
        teachers = db.get_teachers()
        assert len(teachers) == 1
        assert isinstance(teachers[0], Teacher)
        assert teachers[0].name == "John"

    def test_get_teacher(self, teacher: dict, db: Database):
        teacher = db.get_teacher(teacher.get("telegram_id"))
        assert teacher.name == "John"
        assert teacher.telegram_id == 123456789
        assert teacher.username == "john_doe"

    def test_get_students(self, db: Database):
        results = db.get_students()
        assert len(results) == 1
        student, subject = results[0]
        assert isinstance(student, Student)
        assert student.name == "John"
        assert isinstance(subject, Subject)
        assert subject.name == "Math"

    def test_get_student(self, student: dict, db: Database):
        student, subject, group = db.get_student(
            student.get("telegram_id"), student.get("group_name")
        )
        assert student.name == "John"
        assert student.telegram_id == 123456789
        assert group.name == "A"
        assert subject.name == "Math"

    def test_get_subjects(self, db: Database):
        subjects = db.get_subjects()
        assert len(subjects) == 1
        assert isinstance(subjects[0], Subject)
        assert subjects[0].name == "Math"

    def test_get_subject(self, subject: dict, db: Database):
        db_subject = db.get_subject(subject.get("name"))
        assert db_subject.name == "Math"

    def test_get_subjects_by_group(self, db: Database, student: dict):
        subjects = db.get_subjects_by_group(student.get("group_name"))
        assert len(subjects) == 1
        assert isinstance(subjects[0], Subject)
        assert subjects[0].name == "Math"

    def test_get_subjects_by_teacher(self, db: Database, teacher: dict):
        subjects = db.get_subjects_by_teacher(teacher.get("telegram_id"))
        assert len(subjects) == 1
        assert isinstance(subjects[0], Subject)
        assert subjects[0].name == "Math"

    def test_get_groups(self, db: Database):
        groups = db.get_groups()
        assert len(groups) == 2
        assert isinstance(groups[0], Group)
        assert groups[0].name == "A"

    def test_get_group(self, db: Database, student: dict):
        group = db.get_group(student.get("group_name"))
        assert group.name == "A"

    def test_is_teacher(self, teacher: dict, db: Database):
        assert db.is_teacher(teacher.get("telegram_id")) is True

    def test_is_not_teacher(self, db: Database):
        assert db.is_teacher(111) is False

    def test_is_student(self, student: dict, db: Database):
        assert (
            db.is_student(
                student.get("telegram_id"), student.get("group_name")
            )
            is True
        )

    def test_is_not_student(self, db: Database):
        assert db.is_student(111, "A") is False

    def test_drop_all(self, db: Database):
        db.drop_database()
        insp = inspect(db.engine)
        assert insp.has_table("student") is False
        assert insp.has_table("subject") is False
        assert insp.has_table("group") is False
        assert insp.has_table("teacher") is False
