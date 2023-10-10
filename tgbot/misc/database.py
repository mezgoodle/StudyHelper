from tgbot.models.models import Student, Subject, Teacher


class Database:
    def __init__(self):
        self.student = Student
        self.subject = Subject
        self.teacher = Teacher

    async def create_teacher(
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
        return await self.__create_user(
            self.teacher, user_id=user_id, username=username, name=name
        )

    async def create_student(
        self,
        user_id: int,
        username: str | None = None,
        name: str | None = None,
    ):
        """
        Create a new student record.

        Args:
            user_id (int): The ID of the user associated with the student.
            username (str, optional): The username of the student.
                Defaults to None.
            name (str, optional): The name of the student. Defaults to None.

        Returns:
            The created student object.
        """
        return await self.__create_user(
            self.student, user_id=user_id, username=username, name=name
        )

    async def __create_user(
        self,
        db_object: Student | Teacher,
        **kwargs,
    ):
        """
        Creates a new user in the database.

        Args:
            db_object (Student | Teacher): The database object
                used to create the user.
            *args: Additional arguments passed to the create method.

        Returns:
            The result of the create method.
        """
        return await db_object.create(**kwargs)

    async def create_subject(
        self, name: str, description: str, drive_link: str, teacher_id: int
    ) -> Subject:
        """
        Creates a new subject with the given name, description, drive link,
        and teacher ID.

        Args:
            name (str): The name of the subject.
            description (str): The description of the subject.
            drive_link (str): The Google Drive link associated with the subject.
            teacher_id (int): The ID of the teacher responsible for the subject.

        Returns:
            Subject: The newly created Subject object.

        Raises:
            None
        """
        return await self.subject.create(
            name=name,
            description=description,
            drive_link=drive_link,
            teacher_id=teacher_id,
        )

    def get_teachers(self) -> list[Teacher]:
        """
        Get the list of teachers.

        :return: A list of Teacher objects.
        """
        return self.teacher.all()

    def get_students(self) -> list[Student]:
        """
        Returns a list of all students.

        :return: A list of Student objects representing all the students.
        :rtype: list[Student]
        """
        return self.student.all()

    def get_teacher(self, user_id: int) -> Teacher | None:
        """
        Retrieves a teacher based on the provided user ID.

        Parameters:
            user_id (int): The ID of the user for which to retrieve the teacher.

        Returns:
            Teacher | None: The teacher object corresponding to the provided user ID,
            or None if no teacher is found.
        """
        return self.teacher.filter(user_id=user_id).first()

    async def get_subjects_by_teacher_id(
        self, teacher_id: int
    ) -> list[Subject]:
        """
        Retrieves a list of subjects based on a given teacher ID.

        Args:
            teacher_id (int): The ID of the teacher.

        Returns:
            list[Subject]: A list of Subject objects filtered by the given teacher ID.
        """
        return await self.subject.filter(teacher_id=teacher_id).all()
