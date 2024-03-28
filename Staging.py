import time
import krpc

class Staging:
    def run_functions(self, vessel, conn):
        resources = self.get_resources(vessel)
        liquid_fuel_stream = self.create_stream(resources, 'LiquidFuel', conn)
        print("Liquid Fuel Stream:", liquid_fuel_stream)
        liquid_fuel_amount = liquid_fuel_stream()
        print("Current Liquid Fuel Amount:", liquid_fuel_amount)

    def get_resources(self, vessel):
        # Retrieve resources for the current stage
        return vessel.resources_in_decouple_stage(vessel.control.current_stage - 1, cumulative=False)

    def create_stream(self, resources, resource_name, conn):
        # Create a stream to monitor the amount of a specific resource
        resource_amount_stream = conn.add_stream(resources.amount, resource_name)
        return resource_amount_stream

# Example usage:
if __name__ == "__main__":
    conn = krpc.connect(name='Staging Example')
    vessel = conn.space_center.active_vessel
    stager = Staging()
    stager.run_functions(vessel, conn)
