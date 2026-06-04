from time import monotonic

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Digits
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive

class TimeDisplay(Digits):
    start_time = reactive(monotonic)
    time = reactive(0.0)

    def on_mount(self) -> None:
        self.set_interval(1 / 60, self.update_time)

    def update_time(self) -> None:
        self.time = monotonic() - self.start_time

    def watch_time(self, time: float) -> None:
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02.0f}:{minutes:02.0f}:{seconds:05.2f}")

class Stopwatch(HorizontalGroup):
   # o widget de cronometro, que vai agrupar os outros

   def on_button_pressed(self, event: Button.Pressed) -> None:
       # o que deve acontecer quando um botão é pressionado
       if event.button.id == "start":
           self.add_class("started")
       elif event.button.id == "stop":
           self.remove_class("started")

   def compose(self) -> ComposeResult:
       yield Button("Start", id="start", variant="success")
       yield Button("Stop", id="stop", variant="error")
       yield Button("Reset", id="reset")
       yield TimeDisplay()

class StopwatchApp(App):

    CSS_PATH = "stopwatchStyle.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "toggle dark mode")
    ]

    def compose(self) -> ComposeResult:
        # cria widgets para o app (header e footer)
        yield Header()
        yield Footer()
        yield VerticalScroll(Stopwatch())

    def action_toggle_dark(self) -> None:

        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

if __name__ == "__main__":
    app = StopwatchApp()
    app.run()
