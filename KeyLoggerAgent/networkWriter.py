from interfaceManager import*

class NetworkWriter(Iwriter):
    def send_data(self, data: str, machine_name: str) -> None:
        print(f"Sending data to {machine_name}")
        # Send data to the server
        pass