import krpc
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Header, Footer, Button, Static
class Buttons(Static):
    def compose(self) -> ComposeResult:
        """Create Widgets"""
        yield Button("STAGE", id="stage1", variant="success")
        yield Button("STAGE", id="stageclick")
        """
        yield Button("Stage 3")
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
        yield ScrollableContainer(Buttons(), Buttons(), Buttons())

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
