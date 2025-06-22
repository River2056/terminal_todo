from sqlalchemy import Boolean, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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
