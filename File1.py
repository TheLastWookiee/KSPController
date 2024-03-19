import krpc
from textual.app import App, ComposeResult

from textual.containers import ScrollableContainer, Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import Header, Footer, Button, Static, Label

"""box is a widget that allows you to group other widgets together"""
"""
class Buttons(Box):
    def render(self) -> RenderableType:
        return [
            Button("STAGE", id="stage1", variant="success"),
            Button("STAGE2", id="stageclick", style="display:none")
        ]
"""
class KSPcontoller(App):
    """A textual app to control rockets in Kerbal Space Program"""
    CSS_PATH = "coollookingthing.tcss"
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
        yield Container(Label("fuel"), id="fuel")
        yield Container(Label("center top"), id="center-top")
        yield Container(Label("right top"), id="right-top")

        yield Container(Label("center middle"), id="center-middle")
        yield Container(Label("right middle"), id="right-middle")

        yield Container(Label("center bottom"), id="center-bottom")
        yield Container(Vertical(Button("STAGE", id="stage", variant="success")), id="container")


    def action_throttle_up(self) -> None:
        self.throttle_up()

    def action_throttle_down(self) -> None:
        self.throttle_down()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "stage1":
            print("button unpressed")
        elif event.button.id == "stageclick":
            print("button pressed")



if __name__ == "__main__":
    app = KSPcontoller()
    app.run()
