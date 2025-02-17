
class Buffer:

    def __init__(self, __max_size = 200):
        self.__data = []
        self.__max_size = __max_size

    def add_data(self, data: str):
        self.__data.append(data)
        if len(self.__data) > self.__max_size:
            self.__data.pop(0)

    def get_data(self):
        return self.__data

    def flush(self):
        self.__data.clear()

    def is_full(self):
        return len(self.__data) == self.__max_size