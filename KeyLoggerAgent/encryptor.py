import base64

class Encryptor:
    __key = "secretkey1.1"
    def encrypt(self, data: str):
        encrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, self.__key * (len(data) // len(self.__key) + 1)))
        return encrypted

    def decrypt(self, data: str):
        encrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, self.__key * (len(data) // len(self.__key) + 1)))
        return encrypted

encryptor = Encryptor()
encrypted_data = encryptor.encrypt("328951595")
print(encrypted_data)
# decrypt the encrypted data
decrypted_data = encryptor.decrypt(encrypted_data)
print(decrypted_data)

#base64.b64encode(encrypted.encode()).decode()