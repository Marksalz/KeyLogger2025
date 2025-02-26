import os
from dotenv import load_dotenv

class Encryptor:
    """
    A class used to represent an Encryptor that handles encryption and decryption of data.
    """

    def __init__(self, __key=None):
        """
        Initialize a new Encryptor instance.

        Args:
            __key (str, optional): The encryption key.
            If not provided, it will be loaded from the environment variable 'KEY_ENCRYPTION'.
        """
        # Load environment variables from .env file
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
        self.__key = __key or os.getenv("KEY_ENCRYPTION")

    def encrypt(self, data: str):
        """
        Encrypt the given data using the instance's encryption key.

        Args:
            data (str): The data to be encrypted.

        Returns:
            str: The encrypted data.
        """
        encrypted = ''.join(
            chr((ord(c) ^ ord(k))) for c, k in zip(data, self.__key * (len(data) // len(self.__key) + 1)))
        return encrypted

    def decrypt(self, data: str):
        """
        Decrypt the given data using the instance's encryption key.

        Args:
            data (str): The data to be decrypted.

        Returns:
            str: The decrypted data.
        """
        return self.encrypt(data)