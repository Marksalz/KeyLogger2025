import json
import time
from datetime import datetime

from interfaceManager import*
class FileWriter(Iwriter):

    def send_data(self, data: str, machine_name: dict) -> None:
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(f"{next(iter(machine_name))}.txt", "a") as file:
            file.write(json.dumps({"timestamp": time_stamp, "data": data}, indent=4) + "\n")
            file.close()
