class Encryptor:

    def __init__(self, __key = "secretkey1"):
        self.__key = __key

    def encrypt(self, data: str):
        encrypted = ''.join(
            chr((ord(c) ^ ord(k))) for c, k in zip(data, self.__key * (len(data) // len(self.__key) + 1)))
        return encrypted

    def decrypt(self, data: str):
        return self.encrypt(data)

#encryptor = Encryptor()
# encrypted_data = encryptor.encrypt("adina 328951595")
# print(f"Encrypted data: {encrypted_data}")
# decrypted_data = encryptor.decrypt("XUUAUgpUBkUyVApLEAIEFw5FSRFGRVFSU1RdRUERQEVQUldUXw==")
# print(f"Decrypted data: {decrypted_data}")





