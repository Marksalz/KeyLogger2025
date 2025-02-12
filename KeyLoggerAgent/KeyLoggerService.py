from IKeyLogger import *
from typing import List
from pynput import keyboard

class KeyLoggerService(IKeyLogger):
    __buffer = []
    __is_logging = False

    def start_logging(self) -> None:
        self.__is_logging = True



    def stop_logging(self) -> None:
        pass

    def get_logged_keys(self) -> List[str]:
        pass

