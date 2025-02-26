class Buffer:
    """
    A class used to represent a Buffer that stores and manages data.
    """

    def __init__(self):
        """
        Initialize a new Buffer instance.
        """
        self.__data = []

    def add_data(self, data: str):
        """
        Add data to the buffer.

        Args:
            data (str): The data to be added to the buffer.
        """
        self.__data.append(data)

    def get_data(self):
        """
        Retrieve the data from the buffer.

        Returns:
            list: The list of data stored in the buffer.
        """
        return self.__data

    def flush(self):
        """
        Clear all data from the buffer.
        """
        self.__data.clear()
