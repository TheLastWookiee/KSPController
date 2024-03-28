import time

import krpc
from Staging import Staging


class Connector:

    def __init__(self):
        self.connect()

    def connect(self):
        while True:
            try:
                print("Connecting")
                conn = krpc.connect(name='Hello World')
                vessel = conn.space_center.active_vessel
                print(vessel.name)
                staging_instance = Staging()  # Create an instance of Staging
                staging_instance.run_functions(vessel, conn)

                break  # Break out of the loop if connection is successful
            except Exception as e:
                print(f"Error connecting to KRPC server: {e}")
                print("Retrying in 5 seconds...")
                time.sleep(5)  # Wait for 5 seconds before retrying connection


if __name__ == "__main__":
    connector = Connector()
