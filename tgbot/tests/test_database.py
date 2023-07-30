import pytest
from sqlmodel import Session, inspect

from tgbot.models.database import (
    Database,
    Group,
    GroupDB,
    Student,
    StudentDB,
    Subject,
    SubjectDB,
    Teacher,
    TeacherDB,
)


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


@pytest.fixture(name="groupdb")
def groupdb_fixture():
    return GroupDB()


@pytest.fixture(name="studentdb")
def studentdb_fixture():
    return StudentDB()


@pytest.fixture(name="subjectdb")
def subjectdb_fixture():
    return SubjectDB()


@pytest.fixture(name="teacherdb")
def teacherdb_fixture():
    return TeacherDB()


class TestFailOperations:
    def test_create_teacher_fail(self, teacherdb: TeacherDB):
        with pytest.raises(Exception):
            teacherdb.create_teacher()

    def test_create_group_fail(self, groupdb: GroupDB):
        with pytest.raises(Exception):
            groupdb.create_group()

    def test_create_student_fail(self, studentdb: StudentDB, student: dict):
        with pytest.raises(ValueError):
            studentdb.create_student(**student)

    def test_create_subject_fail(self, subjectdb: SubjectDB, subject: dict):
        with pytest.raises(Exception):
            subjectdb.create_subject(**subject)


class TestTeacherDB:
    def test_create_teacher(
        self, session: Session, teacher: dict, teacherdb: TeacherDB
    ):
        teacherdb.create_teacher(**teacher)
        db_teacher = session.query(Teacher).filter_by(name="John").first()
        assert db_teacher.name == teacher.get("name")
        assert db_teacher.telegram_id == teacher.get("telegram_id")
        assert db_teacher.username == teacher.get("username")

    def test_get_teachers(self, teacherdb: TeacherDB):
        teachers = teacherdb.get_teachers()
        assert len(teachers) == 1
        assert isinstance(teachers[0], Teacher)
        assert teachers[0].name == "John"

    def test_get_teacher(self, teacher: dict, teacherdb: TeacherDB):
        teacher = teacherdb.get_teacher(teacher.get("telegram_id"))
        assert teacher.name == "John"
        assert teacher.telegram_id == 123456789
        assert teacher.username == "john_doe"

    def test_is_teacher(self, teacher: dict, teacherdb: TeacherDB):
        assert teacherdb.is_teacher(teacher.get("telegram_id")) is True

    def test_is_not_teacher(self, teacherdb: TeacherDB):
        assert teacherdb.is_teacher(111) is False


class TestGroupDB:
    def test_create_group(
        self, session: Session, groupdb: GroupDB, student: dict
    ):
        groupdb.create_group(student.get("group_name"))
        db_group = session.query(Group).filter_by(name="A").first()
        assert db_group.name == student.get("group_name")

    def test_get_groups(self, groupdb: GroupDB):
        groups = groupdb.get_groups()
        assert len(groups) == 1
        assert isinstance(groups[0], Group)
        assert groups[0].name == "A"

    def test_get_group(self, groupdb: GroupDB, student: dict):
        group = groupdb.get_group(student.get("group_name"))
        assert group.name == "A"


class TestSubjectDB:
    def test_create_subject(
        self,
        session: Session,
        subject: dict,
        student: dict,
        subjectdb: SubjectDB,
    ):
        subjectdb.create_subject(
            **subject, group_name=student.get("group_name")
        )
        db_subject = session.query(Subject).filter_by(name="Math").first()
        assert db_subject.name == subject.get("name")

    # def test_create_subject_and_group(
    #     self,
    #     session: Session,
    #     subject: dict,
    #     student: dict,
    #     subjectdb: SubjectDB,
    # ):
    #     group_in_db = session.query(Group).filter_by(name="A").first()
    #     assert group_in_db is not None
    #     session.delete(group_in_db)
    #     session.commit()

    #     subjectdb.create_subject(
    #         **subject, group_name=student.get("group_name")
    #     )
    #     db_subject = session.query(Subject).filter_by(name="Math").first()
    #     assert db_subject.name == subject.get("name")

    def test_get_subjects(self, subjectdb: SubjectDB):
        subjects = subjectdb.get_subjects()
        assert len(subjects) == 1
        assert isinstance(subjects[0], Subject)
        assert subjects[0].name == "Math"

    def test_get_subject(self, subject: dict, subjectdb: SubjectDB):
        db_subject, db_group = subjectdb.get_subject(subject.get("name"))
        assert db_subject.name == "Math"
        assert db_group.name == "A"

    def test_get_subjects_by_group(self, subjectdb: SubjectDB, student: dict):
        subjects = subjectdb.get_subjects_by_group(student.get("group_name"))
        assert len(subjects) == 1
        assert isinstance(subjects[0], Subject)
        assert subjects[0].name == "Math"

    def test_get_subjects_by_non_existing_group(self, subjectdb: SubjectDB):
        with pytest.raises(ValueError):
            subjectdb.get_subjects_by_group("non_existing_group")

    def test_get_subjects_by_teacher(
        self, subjectdb: SubjectDB, teacher: dict
    ):
        subjects = subjectdb.get_subjects_by_teacher(
            teacher.get("telegram_id")
        )
        assert len(subjects) == 1
        assert isinstance(subjects[0], Subject)
        assert subjects[0].name == "Math"

    def test_get_subjects_by_non_existing_teacher(self, subjectdb: SubjectDB):
        with pytest.raises(ValueError):
            subjectdb.get_subjects_by_teacher(111)


class TestStudentDB:
    def test_create_student(
        self, session: Session, student: dict, studentdb: StudentDB
    ):
        studentdb.create_student(**student)
        db_student = session.query(Student).filter_by(name="John").first()
        assert db_student.name == student.get("name")
        assert db_student.telegram_id == student.get("telegram_id")
        assert db_student.group.name == student.get("group_name")

    def test_create_student_with_non_existing_group(
        self, student: dict, studentdb: StudentDB, session: Session
    ):
        # create temporary subject
        subject = Subject(name="Math")
        session.add(subject)
        session.commit()
        with pytest.raises(ValueError, match="Group is not created"):
            studentdb.create_student(
                name=student.get("name"),
                telegram_id=student.get("telegram_id"),
                username=student.get("username"),
                subject_name=student.get("subject_name"),
                group_name="non_existing_group",
            )
        # delete temporary subject
        session.delete(subject)
        session.commit()

    def test_create_student_with_non_existing_subject(
        self, student: dict, studentdb: StudentDB
    ):
        with pytest.raises(ValueError, match="Subject is not created"):
            studentdb.create_student(
                name=student.get("name"),
                telegram_id=student.get("telegram_id"),
                username=student.get("username"),
                subject_name="non_existing_subject",
                group_name=student.get("group_name"),
            )

    def test_get_students(self, studentdb: StudentDB):
        results = studentdb.get_students()
        assert len(results) == 1
        student, subject = results[0]
        assert isinstance(student, Student)
        assert student.name == "John"
        assert isinstance(subject, Subject)
        assert subject.name == "Math"

    def test_get_student(self, student: dict, studentdb: StudentDB):
        student, subject, group = studentdb.get_student(
            student.get("telegram_id"), student.get("group_name")
        )
        assert student.name == "John"
        assert student.telegram_id == 123456789
        assert group.name == "A"
        assert subject.name == "Math"

    def test_is_student(self, student: dict, studentdb: StudentDB):
        assert (
            studentdb.is_student(
                student.get("telegram_id"), student.get("group_name")
            )
            is True
        )

    def test_is_not_student(self, studentdb: StudentDB):
        assert studentdb.is_student(111, "A") is False


class TestDatabase:
    def test_drop_all(self, db: Database):
        db.drop_database()
        insp = inspect(db.engine)
        assert insp.has_table("student") is False
        assert insp.has_table("subject") is False
        assert insp.has_table("group") is False
        assert insp.has_table("teacher") is False
