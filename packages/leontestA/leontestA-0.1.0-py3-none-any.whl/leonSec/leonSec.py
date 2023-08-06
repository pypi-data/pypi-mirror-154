import os
from time import sleep


class leon:
    def command(command,name):
        print(f"hello {name} yor command have been recived")
        sleep(2)
        os.system(command)
        print("command exected")

