import requests
from interfaceManager import*

class NetworkWriter(Iwriter):
    def __init__(self, url: str):
        self.__url = url

    def send_data(self, data: str, machine_name: dict) -> None:
        print(f"Sending data to {machine_name}")
        # Send data to the server
        response = requests.post(self.__url, json={"machine": machine_name, "data": data})
        if response.status_code != 200:
            print(f"Failed to send data to {machine_name}")
        else:
            print(f"Data sent to {machine_name}")
            print(response.json())

