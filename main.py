from datetime import datetime
from textual.app import App
from textual import on
from textual.containers import Container, HorizontalGroup, VerticalScroll
from textual.widgets import Button, Checkbox, Digits, Header, Footer, Input

from models.models import TaskManager


class TodoApp(App):

    CSS_PATH = "styles.tcss"

    BINDINGS = [("q", "quit", "Quit")]

    command = ""
    content = ""
    task_manager = TaskManager()

    btns = None
    input_box = Input(placeholder="stuff you want to do", id="input_box")
    tasks = task_manager.get()

    def compose(self):
        yield Header(show_clock=True)
        with Container(classes="clock"):
            yield Digits("")

        with HorizontalGroup(id="btns"):
            yield Button(id="add", label="add")
            yield Button(id="del", label="del")
        yield self.input_box
        with VerticalScroll(id="todos"):
            for task in self.tasks:
                yield Checkbox(id=task.id, label=task.content, value=task.done)

        yield Footer()

    def on_ready(self):
        self.update_clock()
        self.set_interval(1, self.update_clock)

    def update_clock(self):
        now = datetime.now().time()
        self.query_one(Digits).update(f"{now:%T}")

    def on_mount(self):
        input_box = self.query_one("#input_box")
        input_box.add_class("hide")
        self.btns = self.query_one("#btns", HorizontalGroup)

    @on(Button.Pressed)
    async def handle_btn_pressed(self, event: Button.Pressed):
        btn_id = event.button.id
        if self.input_box.has_class("hide"):
            match btn_id:
                case "add":
                    self.command = "add"
                    self.toggle()
                    self.input_box.focus()
                case "del":
                    self.command = "del"
                    await self.handle_command()

    @on(Input.Submitted, "#input_box")
    async def on_enter_content(self, event: Input.Submitted):
        self.content = event.value
        self.input_box.value = ""
        self.toggle()

        await self.handle_command()

    @on(Checkbox.Changed)
    def handle_mark(self, event: Checkbox.Changed):
        assert event.checkbox.id is not None
        task_id = event.checkbox.id
        done = event.value
        self.task_manager.mark_as_done(task_id, done)

    async def handle_command(self):
        match (self.command):
            case "add":
                self.task_manager.add(self.content)
                self.tasks = self.task_manager.get()
                await self.refresh_tasks()
            case "del":
                for done_task in filter(lambda x: x.done, self.tasks):
                    self.task_manager.delete(done_task.id)
                self.tasks = self.task_manager.get()
                await self.refresh_tasks()

    async def refresh_tasks(self):
        container = self.query_one("#todos", VerticalScroll)
        await container.remove_children()
        for task in self.tasks:
            check = Checkbox(id=task.id, label=task.content, value=task.done)
            container.mount(check)

    def toggle(self):
        if self.btns.has_class("hide"):  # type: ignore
            self.btns.remove_class("hide")  # type: ignore
            self.input_box.add_class("hide")
        else:
            self.btns.add_class("hide")  # type: ignore
            self.input_box.remove_class("hide")


if __name__ == "__main__":
    todoApp = TodoApp()
    todoApp.run()
