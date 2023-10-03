from tgbot.models.models import Student, Subject, Teacher


class Database:
    def __init__(self):
        self.student = Student
        self.subject = Subject
        self.teacher = Teacher

    def create_teacher(
        self,
        user_id: int,
        username: str | None = None,
        name: str | None = None,
    ):
        """
        Creates a teacher with the given user ID, username, and name.

        Parameters:
            user_id (int): The ID of the user.
            username (str | None, optional): The username of the teacher. Defaults to None.
            name (str | None, optional): The name of the teacher. Defaults to None.

        Returns:
            The created teacher object.
        """  # noqa: E501
        return self.__create_user(
            self.teacher, Teacher, user_id, username, name
        )

    def create_student(
        self,
        user_id: int,
        username: str | None = None,
        name: str | None = None,
    ):
        """
        Create a new student record.

        Args:
            user_id (int): The ID of the user associated with the student.
            username (str, optional): The username of the student. Defaults to None.
            name (str, optional): The name of the student. Defaults to None.

        Returns:
            The created student object.
        """
        return self.__create_user(
            self.student, Student, user_id, username, name
        )

    def __create_user(
        self,
        db_object: Student | Teacher,
        *args,
    ):
        """
        Creates a new user in the database.

        Args:
            db_object (Student | Teacher): The database object used to create the user.
            *args: Additional arguments passed to the create method.

        Returns:
            The result of the create method.
        """
        return db_object.create(*args)

    def get_teachers(self) -> list[Teacher]:
        return self.teacher.all()

    def get_students(self) -> list[Student]:
        return self.student.all()
