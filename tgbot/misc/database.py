from datetime import date

from tgbot.models.models import (
    Solution,
    Student,
    Subject,
    SubjectTask,
    Teacher,
)


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
        self, name: str, description: str, teacher_id: int
    ) -> Subject | None:
        return await self.subject.create(
            name=name,
            description=description,
            teacher_id=teacher_id,
        )

    async def create_solution(
        self, subject_task_id: int, student_id: int, file_link: str
    ) -> Solution | None:
        subject_task = await self.get_subject_task(subject_task_id)
        student = await self.get_student(student_id)
        return await self.solution.create(
            subject_task=subject_task, student=student, file_link=file_link
        )

    async def create_subject_task(
        self,
        name: str,
        description: str,
        due_date: date,
        subject_id: int,
        task_id: int | None = None,
    ) -> SubjectTask | None:
        subject = await self.get_subject(subject_id)
        new_task, _ = await self.subjecttask.update_or_create(
            defaults={
                "name": name,
                "description": description,
                "due_date": due_date,
            },
            subject=subject,
            pk=task_id,
        )
        return new_task

    async def get_solutions_for_task(
        self, subject_task_id: int
    ) -> list[Solution]:
        return (
            await self.solution.filter(subject_task_id=subject_task_id)
            .all()
            .prefetch_related("student")
        )

    async def get_count_solutions_by_subject(
        self, subject: Subject
    ) -> dict[str, int]:
        students = await self.student.filter(subjects=subject).count()
        tasks = await self.subjecttask.filter(subject=subject).all()
        stats = {}
        for task in tasks:
            solutions = await self.solution.filter(subject_task=task).count()
            stats[task.name] = solutions / students
        return stats

    async def get_student_solution(
        self, student_id: int, subject_task_id: int
    ) -> Solution | None:
        student = await self.get_student(student_id)
        subject_task = await self.get_subject_task(subject_task_id)
        return (
            await self.solution.filter(
                student=student.id, subject_task=subject_task.id
            )
            .first()
            .prefetch_related("student", "subject_task__subject__teacher")
        )

    async def update_solution_grade(
        self, solution_id: int, grade: int
    ) -> Solution | None:
        rows_affected = await self.solution.filter(id=solution_id).update(
            grade=grade
        )

        if rows_affected > 0:
            updated_solution = (
                await self.solution.filter(id=solution_id)
                .first()
                .prefetch_related("student", "subject_task")
            )
            return updated_solution
        return None

    async def update_solution_file_link(
        self, solution: Solution, new_file_link: str
    ) -> bool:
        rows_affected = await self.solution.filter(id=solution.id).update(
            file_link=new_file_link
        )
        return rows_affected > 0

    async def is_student(self, user_id: int) -> bool:
        return await self.student.filter(user_id=user_id).exists()

    async def is_teacher(self, user_id: int) -> bool:
        return await self.teacher.filter(user_id=user_id).exists()

    async def get_teachers(self) -> list[Teacher]:
        return await self.teacher.all()

    async def get_students(self) -> list[Student]:
        return await self.student.all()

    async def get_teacher(self, user_id: int) -> Teacher | None:
        return await self.teacher.filter(user_id=user_id).first()

    async def get_subject(self, subject_id: int) -> Subject | None:
        return await self.subject.filter(id=subject_id).first()

    async def get_subject_task(
        self, subject_task_id: int
    ) -> SubjectTask | None:
        return (
            await self.subjecttask.filter(id=subject_task_id)
            .first()
            .prefetch_related("subject", "subject__teacher")
        )

    async def get_student(self, user_id: int) -> Student | None:
        return await self.student.filter(user_id=user_id).first()

    async def get_subjects_by_teacher_id(
        self, teacher_id: int
    ) -> list[Subject]:
        return await self.subject.filter(teacher_id=teacher_id).all()

    async def get_student_subjects(self, student: Student) -> list[Subject]:
        return await student.subjects
