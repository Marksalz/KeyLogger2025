
class Buffer:

    def __init__(self):
        self.__data = []

    def add_data(self, data: str):
        self.__data.append(data)

    def get_data(self):
        return self.__data

    def flush(self):
        self.__data.clear()
