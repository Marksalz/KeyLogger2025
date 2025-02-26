import requests
from interfaceManager import *


class NetworkWriter(Iwriter):
    """
    A class used to send data to a server over the network.

    Inherits from:
        Iwriter: An interface that defines the send_data method.
    """

    def __init__(self, url: str):
        """
        Initialize a new NetworkWriter instance.

        Args:
            url (str): The URL of the server to which data will be sent.
        """
        self.__url = url

    def send_data(self, data: str, machine_name: dict) -> None:
        """
        Send the provided data to the server.

        Args:
            data (str): The data to be sent to the server.
            machine_name (dict): A dictionary containing the machine name as the key.

        Returns:
            None
        """
        print(f"Sending data to {machine_name}")
        # Send data to the server
        response = requests.post(self.__url, json={"machine": machine_name, "data": data})
        if response.status_code != 200:
            print(f"Failed to send data to {machine_name}")
        else:
            print(f"Data sent to {machine_name}")
            print(response.json())
