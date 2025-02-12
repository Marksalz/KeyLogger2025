from interfaceManager import*
class FileWriter(Iwriter):


    def send_data(self, data: str, machine_name: str) -> None:
        with open(f"{machine_name}.txt", "a") as file:
            file.write(data)
            file.write("\n")
            file.close()
