import pytest
from sqlmodel import Session

from tgbot.models.database import Database, Student, Teacher


@pytest.fixture(name="db")
def db_fixture():
    db = Database()
    return db


@pytest.fixture(name="session")
def session_fixture(db: Database):
    with Session(db.engine) as session:
        yield session


@pytest.fixture(name="student")
def valid_student():
    return {
        "name": "John",
        "telegram_id": 123456789,
        "group": "A",
        "username": "john_doe",
        "subject_name": "Math",
    }


@pytest.fixture(name="subject")
def valid_subject():
    return {"name": "Math"}


@pytest.fixture(name="teacher")
def valid_teacher():
    return {
        "name": "John",
        "telegram_id": 123456789,
        "username": "john_doe",
    }


class TestSimpleQueries:
    def test_create_student(self, session: Session, student: dict, db: Database):
        db.create_student(**student)
        db_student = session.query(Student).filter_by(name="John").first()
        assert db_student.name == student.get("name")
        assert db_student.telegram_id == student.get("telegram_id")
        assert db_student.group == student.get("group")

    def test_create_teacher(self, session: Session, teacher: dict, db: Database):
        db.create_teacher(**teacher)
        db_teacher = session.query(Teacher).filter_by(name="John").first()
        assert db_teacher.name == teacher.get("name")
        assert db_teacher.telegram_id == teacher.get("telegram_id")
        assert db_teacher.username == teacher.get("username")

    def test_get_teacher(self, teacher: dict, db: Database):
        teacher = db.get_teacher(teacher.get("telegram_id"))
        assert teacher.name == "John"
        assert teacher.telegram_id == 123456789
        assert teacher.username == "john_doe"

    def test_get_student(self, student: dict, db: Database):
        student = db.get_student(student.get("telegram_id"))
        assert student.name == "John"
        assert student.telegram_id == 123456789
        assert student.group == "A"

    def test_get_subject(self, subject: dict, db: Database):
        subject = db.get_subject(subject.get("name"))
        assert subject is None

    def test_is_teacher(self, teacher: dict, db: Database):
        assert db.is_teacher(teacher.get("telegram_id")) is True

    # @pytest.mark.xfail(raises=IntegrityError)
    # def test_author_no_email(self, db_session):
    #     author = Author(firstname="James", lastname="Clear")
    #     db_session.add(author)
    #     try:
    #         db_session.commit()
    #     except IntegrityError:
    #         db_session.rollback()

    # def test_article_valid(self, db_session, valid_author):
    #     valid_article = Article(
    #         slug="sample-slug",
    #         title="Title of the Valid Article",
    #         content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    #         author=valid_author,
    #     )
    #     db_session.add(valid_article)
    #     db_session.commit()
    #     sample_article = db_session.query(Article).filter_by(slug="sample-slug").first()
    #     assert sample_article.title == "Title of the Valid Article"
    #     assert len(sample_article.content.split(" ")) > 50


class TestComplexQueries:
    pass
