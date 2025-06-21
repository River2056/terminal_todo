from uuid import uuid4

from sqlalchemy import Boolean, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from . import engine


class Base(DeclarativeBase):
    pass


class Task(Base):
    """
    A simple class representing a todo task
    """

    __tablename__ = "TASK"
    id: Mapped[str] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String)
    done: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self):
        return f"Task[id: {self.id}, content: {self.content}, done: {self.done}]"


Task.metadata.create_all(engine)


class TaskManager:
    """
    A Task Manager for managing todo tasks
    """

    def __init__(self):
        self.tasks = []
        self.session = Session(engine)

    def get(self, id="") -> list[Task]:
        """
        Gets task from list, if have specific id, fetch out the task, else return all tasks
        """
        if id == "":
            return self.session.query(Task).all()
        else:
            return self.session.query(Task).filter(Task.id == id).all()

    def add(self, task_content: str) -> str:
        """
        Adds a task to list, returns the id.
        """
        added_id = f"task-{str(uuid4())}"

        task = Task(id=added_id, content=task_content, done=False)
        with self.session as session:
            session.add(task)
            session.commit()

        return added_id

    def mark_as_done(self, id: str, done=True) -> bool:
        """
        Marks a task as done, can pass in custom done args to toggle the task's done status.
        returns True if task successfully updated, False otherwise.
        """
        try:
            task: Task | None = self.session.query(Task).filter(Task.id == id).first()
            assert task is not None
            task.done = done
            self.session.add(task)
            self.session.commit()
            return True
        except Exception:
            return False

    def delete(self, id: str) -> None:
        """
        Removes the task from the list
        """
        task: Task | None = self.session.query(Task).filter(Task.id == id).first()
        assert task is not None
        self.session.query(Task).filter(Task.id == id).delete()
        self.session.commit()

    def update(self, id, new_content: str) -> bool:
        """
        Updates a task's content, returns True if successfully updated, False otherwise
        """
        try:
            task: Task | None = self.session.query(Task).filter(Task.id == id).first()
            assert task is not None
            task.content = new_content
            self.session.add(task)
            self.session.commit()
            return True
        except Exception:
            return False
