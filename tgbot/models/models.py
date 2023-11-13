from tortoise import Tortoise, fields

from tgbot.models.base import TimedBaseModel

db = Tortoise()


class User(TimedBaseModel):
    name = fields.CharField(max_length=255, null=True, description="User name")
    user_id = fields.IntField(
        unique=True,
        description="Telegram user id",
        index=True,
    )
    username = fields.CharField(
        max_length=255,
        null=True,
        description="Telegram username",
        unique=True,
    )
    subjects: fields.ManyToManyRelation["Subject"]

    class Meta:
        abstract = True


class Teacher(User):
    pass


class Student(User):
    solutions: fields.ReverseRelation["Solution"]


class Subject(TimedBaseModel):
    name = fields.CharField(max_length=255, description="Subject name")
    description = fields.TextField(null=True)
    teacher: fields.ForeignKeyRelation[Teacher] = fields.ForeignKeyField(
        "models.Teacher",
        related_name="subjects",
        description="Subject teacher",
    )
    students: fields.ManyToManyRelation[Student] = fields.ManyToManyField(
        "models.Student",
        related_name="subjects",
        description="Subject students",
    )
    drive_link = fields.CharField(
        max_length=255,
        null=True,
        description="Drive link",
    )
    tasks: fields.ReverseRelation["SubjectTask"]

    def __str__(self):
        return self.name


class Task(TimedBaseModel):
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    due_date = fields.DatetimeField(
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SubjectTask(Task):
    subject: fields.ForeignKeyRelation[Subject] = fields.ForeignKeyField(
        "models.Subject", related_name="tasks", description="Task subject"
    )


class Solution(TimedBaseModel):
    subject_task: fields.ForeignKeyRelation[SubjectTask] = fields.ForeignKeyField(
        "models.SubjectTask",
        related_name="students",
        description="Task subject",
        on_delete=fields.OnDelete.CASCADE,
    )
    grade = fields.IntField(
        null=True,
        description="Task grade",
        default=0,
    )
    student: fields.ForeignKeyRelation[Student] = fields.ForeignKeyField(
        "models.Student",
        related_name="tasks",
        description="Task student",
        on_delete=fields.OnDelete.CASCADE,
    )
    file_link = fields.CharField(
        max_length=255,
        null=True,
        description="Task file link",
    )


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "tgbot.models.models"
    await db.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["tgbot.models.models"]},
    )
    # Generate the schema
    await Tortoise.generate_schemas()


async def close_db():
    await db.close_connections()
