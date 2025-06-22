from datetime import datetime
from textual.app import App
from textual import on, events
from textual.containers import Container, VerticalScroll
from textual.widgets import Checkbox, Digits, Header, Footer, Input, Label

from models.task import TaskManager
from models.weather import WeatherManager


class TodoApp(App):

    CSS_PATH = "styles.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("a", "add", "Add new task"),
        ("d", "delete", "Delete completed tasks"),
    ]

    command = ""
    content = ""
    task_manager = TaskManager()
    weather_manager = WeatherManager()

    input_box = Input(placeholder="stuff you want to do", id="input_box")
    tasks = task_manager.get()

    def compose(self):
        yield Header(show_clock=True)
        with Container(classes="clock"):
            yield Digits("")
        with Container(classes="weather-info"):
            yield Label(id="weather")

        yield self.input_box
        with VerticalScroll(id="todos"):
            for task in self.tasks:
                yield Checkbox(id=task.id, label=task.content, value=task.done)

        yield Footer()

    def on_ready(self):
        self.update_clock()
        self.update_weather()
        self.set_interval(1, self.update_clock)
        self.set_interval(2 * 60, self.update_weather)
        self.query_one("#input_box").add_class("hide")

    def update_clock(self):
        now = datetime.now().time()
        self.query_one(Digits).update(f"{now:%T}")

    def update_weather(self):
        weather = self.weather_manager.fetch_weather()
        render_str = f"{weather.name}, {weather.temperature}, {weather.text}"
        self.query_one("#weather", Label).update(render_str)

    def on_key(self, event: events.Key):
        if event.key == "escape" and not self.input_box.has_class("hide"):
            self.toggle()

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

    def action_add(self):
        self.command = "add"
        self.toggle()
        self.input_box.focus()

    async def action_delete(self):
        for done_task in filter(lambda x: x.done, self.tasks):
            self.task_manager.delete(done_task.id)
        self.tasks = self.task_manager.get()
        await self.refresh_tasks()

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
        if self.input_box.has_class("hide"):
            self.input_box.remove_class("hide")
        else:
            self.input_box.add_class("hide")


if __name__ == "__main__":
    todoApp = TodoApp()
    todoApp.run()
