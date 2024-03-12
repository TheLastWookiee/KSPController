import krpc
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static


class KSPcontoller(App):
    """A textual app to control rockets in Kerbal Space Program"""
    BINDINGS = [
        ("z", "throttle_up", "increases the throttle"),
        ("x", "throttle_down", "decreases the throttle")
    ]

    def connect(self):
        conn = krpc.connect(name='Hello World')
        vessel = conn.space_center.active_vessel
        print(vessel.name)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def action_throttle_up(self) -> None:
        self.throttle_up()

    def action_throttle_down(self) -> None:
        self.throttle_down()




class Buttons(Static):
    def compose(self) -> ComposeResult:
        """Create Widgets"""
        yield Button("Stage 1", id="stage1", variant="success")
        yield Button("Stage 2")
        yield Button("Stage 3")


if __name__ == "__main__":
    app = KSPcontoller()
    app.run()
