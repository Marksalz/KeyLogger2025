import os
from dotenv import load_dotenv

class Encryptor:

    def __init__(self, __key=None):
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))  # Load environment variables from .env file
        self.__key = __key or os.getenv("KEY_ENCRYPTION")

    def encrypt(self, data: str):
        encrypted = ''.join(
            chr((ord(c) ^ ord(k))) for c, k in zip(data, self.__key * (len(data) // len(self.__key) + 1)))
        return encrypted

    def decrypt(self, data: str):
        return self.encrypt(data)

# Example usage:
# encryptor = Encryptor()
# encrypted_data = encryptor.encrypt("adina 328951595")
# print(f"Encrypted data: {encrypted_data}")
# decrypted_data = encryptor.decrypt(encrypted_data)
# print(f"Decrypted data: {decrypted_data}")





