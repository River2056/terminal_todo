from uuid import uuid4


class Task:
    """
    A simple class representing a todo task
    """

    def __init__(self, id, content):
        self.id = id
        self.content = content
        self.done = False

    def __repr__(self):
        return f"Task[id: {self.id}, content: {self.content}, done: {self.done}]"


class TaskManager:
    """
    A Task Manager for managing todo tasks
    """

    def __init__(self):
        self.tasks = []

    def get(self, id="") -> list[Task]:
        """
        Gets task from list, if have specific id, fetch out the task, else return all tasks
        """
        if id == "":
            return self.tasks
        else:
            return list(filter(lambda x: x.id == id, self.tasks))[0]

    def add(self, task_content: str) -> str:
        """
        Adds a task to list, returns the id.
        """
        added_id = f"task-{str(uuid4())}"

        task = Task(added_id, task_content)
        self.tasks.append(task)
        return added_id

    def mark_as_done(self, id: str, done=True) -> bool:
        """
        Marks a task as done, can pass in custom done args to toggle the task's done status.
        returns True if task successfully updated, False otherwise.
        """
        for task in self.tasks:
            if task.id == id:
                task.done = done
                return True

        return False

    def delete(self, id: str) -> None:
        """
        Removes the task from the list
        """
        self.tasks = list(filter(lambda x: x.id != id, self.tasks))

    def update(self, id, new_content: str) -> bool:
        """
        Updates a task's content, returns True if successfully updated, False otherwise
        """
        for task in self.tasks:
            if task.id == id:
                task.content = new_content
                return True

        return False
