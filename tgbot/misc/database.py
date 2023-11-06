from tgbot.models.models import Solution, Student, Subject, SubjectTask, Teacher


class Database:
    def __init__(self):
        self.student = Student
        self.subject = Subject
        self.teacher = Teacher
        self.solution = Solution
        self.subjecttask = SubjectTask

    async def create_teacher(
        self,
        user_id: int,
        username: str | None = None,
        name: str | None = None,
    ):
        return await self.__create_user(
            self.teacher, user_id=user_id, username=username, name=name
        )

    async def create_student(
        self,
        user_id: int,
        username: str | None = None,
        name: str | None = None,
    ):
        return await self.__create_user(
            self.student, user_id=user_id, username=username, name=name
        )

    async def __create_user(
        self,
        db_object: Student | Teacher,
        **kwargs,
    ):
        return await db_object.create(**kwargs)

    async def create_subject(
        self, name: str, description: str, drive_link: str, teacher_id: int
    ) -> Subject | None:
        return await self.subject.create(
            name=name,
            description=description,
            drive_link=drive_link,
            teacher_id=teacher_id,
        )

    async def create_solution(
        self, subject_id: int, student_id: int, file_link: str
    ) -> Solution | None:
        subject_task = await self.subjecttask.filter(subject=subject_id).first()
        student = await self.get_student(student_id)
        return await self.solution.create(
            subject_task=subject_task, student=student, file_link=file_link
        )

    async def create_subject_task(
        self,
        name: str,
        description: str,
        due_date: str,
        subject_id: int,
    ) -> SubjectTask | None:
        subject = await self.get_subject(subject_id)
        return await self.subjecttask.create(
            name=name,
            description=description,
            due_date=due_date,
            subject=subject,
        )

    def get_teachers(self) -> list[Teacher]:
        return self.teacher.all()

    def get_students(self) -> list[Student]:
        return self.student.all()

    def get_teacher(self, user_id: int) -> Teacher | None:
        return self.teacher.filter(user_id=user_id).first()

    def get_subject(self, subject_id: int) -> Subject | None:
        return self.subject.filter(id=subject_id).first()

    def get_student(self, user_id: int) -> Student | None:
        return self.student.filter(user_id=user_id).first()

    async def get_subjects_by_teacher_id(self, teacher_id: int) -> list[Subject]:
        return await self.subject.filter(teacher_id=teacher_id).all()

    async def get_student_subjects(self, student: Student) -> list[Subject]:
        return await student.subjects
