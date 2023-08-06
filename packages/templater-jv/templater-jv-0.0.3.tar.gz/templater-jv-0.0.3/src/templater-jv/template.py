#
# by John Vxlan (c) 2022
#

from sys import exit
from os.path import exists

class Template():
    data = ""

    def __init__(self, file):
        if exists(file):
            self.file = file
        else:
            exit("File Not Found: " + file)

    def generate_host(self, collection):
        try:
            with open(self.file, 'r') as fp:
                for line in fp:
                    for key, value in collection.items():
                        if key in line:
                            line = line.replace(key, value)
                    self.data += line

            fp.close()
            print(self.data)
        except FileNotFoundError:
            print("File Not Found: " + self.file)
