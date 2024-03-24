import threading
import time

import krpc
from textual.app import App, ComposeResult, CSSPathType

from textual.containers import ScrollableContainer, Container, Horizontal, Vertical
from textual.driver import Driver
from textual.reactive import reactive
from textual.widgets import Header, Footer, Button, Static, Label, ProgressBar

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

    def __init__(
            self,
            driver_class: type[Driver] | None = None,
            css_path: CSSPathType | None = None,
            watch_css: bool = False,
    ):
        super().__init__(driver_class, css_path, watch_css)
        self.connect()
        self.vessel = None
        self.previous_fuel_level = 0.0
        """self.start_fuel_monitor()"""

        self._fuel_value = 0
        self.fuel_value = reactive(self._fuel_value)
        self.fuel_monitor()



    def connect(self):
        while True:
            try:
                print("Connecting")
                conn = krpc.connect(name='Hello World')
                self.vessel = conn.space_center.active_vessel
                print(self.vessel.name)

                active_engines = [Engine for Engine in self.vessel.parts.engines if
                                  Engine.active and Engine.has_fuel and Engine.part.stage == self.vessel.control.current_stage]
                for engine in active_engines:
                    print("Engine:", engine.part.name)
                    # Filter propellants to only include liquid fuel
                    liquid_fuel_propellants = [propellant for propellant in engine.propellants if
                                               propellant.name == 'LiquidFuel']
                    total_liquid_fuel_amount = self.vessel.resources_in_decouple_stage(
                        self.vessel.control.current_stage - 1).amount("LiquidFuel")
                    print("  - Total Liquid Fuel:", total_liquid_fuel_amount)
                    #0.0015139278257265685
                    #0.0015518637374043465

                break  # Break out of the loop if connection is successful
            except Exception as e:
                print(f"Error connecting to KRPC server: {e}")
                print("Retrying in 5 seconds...")
                time.sleep(5)  # Wait for 5 seconds before retrying connection
    """@reactive
    def fuel_level(self):
        if hasattr(self, 'vessel'):
            return self.vessel.resources.amount('LiquidFuel') / self.vessel.resources.max('LiquidFuel')
        return 0.0"""

    """def start_fuel_monitor(self):
        time.sleep(9)  # Adjust the delay as needed

        #threading to monitor fuel
        self.fuel_monitor_thread = threading.Thread(target=self.fuel_monitor, daemon=True)
        self.fuel_monitor_thread.start()"""
    def fuel_monitor(self):
        while True:
            self.fuel_down()
    def fuel_down(self):
        # add parentheses instead so that the return value is called and not just the method
        fuel_level = self.vessel.resources_in_decouple_stage(
                            self.vessel.control.current_stage - 1).amount("LiquidFuel")
        fuel_decreasing = self.previous_fuel_level > fuel_level
        self.previous_fuel_level = fuel_level
        if fuel_decreasing:
            self.query_one(ProgressBar).advance(-1)
        self.fuel_value = fuel_level


    def compose(self) -> ComposeResult:
        self.connect()
        yield Header()
        yield Footer()
        yield Container(ProgressBar(total=100))
        yield Container(Label(self.fuel_value), id="fuel")
        yield Container(Label("center top"), id="center-top")
        yield Container(Label("right top"), id="right-top")

        yield Container(Label("center middle"), id="center-middle")
        yield Container(Label("right middle"), id="right-middle")

        yield Container(Label("center bottom"), id="center-bottom")
        yield Container(

            (Button("STAGE", id="stage", variant="success")), id="bottom-right")
        self.fuel_down()

    """def current_stage_isp(self):
        active_engines = [Engine for Engine in self.vessel.parts.engines if Engine.active and Engine.has_fuel and Engine.part.stage == self.vessel.control.current_stage]
        print(active_engines)
        if not active_engines:
            return 0
        thrust = sum(engine.thrust for engine in active_engines)
        fuel_consumption = sum(engine.thrust / engine.specific_impulse
                               for engine in active_engines)
        isp = thrust / fuel_consumption
        return isp"""

    def action_start(self) -> None:
        """Start the progress tracking."""
        self.query_one(ProgressBar).update(total=100)

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
