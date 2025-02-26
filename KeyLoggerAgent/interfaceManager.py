from abc import ABC, abstractmethod
from typing import List


class IKeyLogger(ABC):
    """
    An abstract base class that defines the interface for a keyLogger.
    """

    @abstractmethod
    def start_logging(self) -> None:
        """
        Start logging keystrokes.

        Returns:
            None
        """
        pass

    @abstractmethod
    def stop_logging(self) -> None:
        """
        Stop logging keystrokes.

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_logged_keys(self) -> List[str]:
        """
        Retrieve the logged keystrokes.

        Returns:
            List[str]: A list of logged keystrokes.
        """
        pass


class Iwriter(ABC):
    """
    An abstract base class that defines the interface for a writer.
    """

    @abstractmethod
    def send_data(self, data: str, machine_name: str | dict) -> None:
        """
        Send data to a specified destination.

        Args:
            data (str): The data to be sent.
            machine_name (str | dict): The name of the machine or a dictionary containing machine details.

        Returns:
            None
        """
        pass
