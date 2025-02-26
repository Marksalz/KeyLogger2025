import json
from datetime import datetime
from interfaceManager import *


class FileWriter(Iwriter):
    """
    A class used to write data to a file with a timestamp.

    Inherits from:
        Iwriter: An interface that defines the send_data method.
    """

    def send_data(self, data: str, machine_name: dict) -> None:
        """
        Write the provided data to a file named after the machine.

        Args:
            data (str): The data to be written to the file.
            machine_name (dict): A dictionary containing the machine name as the key.

        Returns:
            None
        """
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(f"{next(iter(machine_name))}.txt", "a") as file:
            file.write(json.dumps({"timestamp": time_stamp, "data": data}, indent=4) + "\n")
            file.close()
