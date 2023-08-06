#
# by John Vxlan (c) 2022
#

from asyncio import exceptions
from logging import exception


class Variables():
    variables = {}
    number_of_variables = 0
    number_of_hosts = 0

    def __init__(self, file):
        try:
            with open(file, 'r') as fp:
                for line in fp:
                    line = line.strip().rstrip()
                    if line and line[0] != '#':
                        if line[0] == '$':
                            current_variable = line
                            self.variables[current_variable] = []
                        else:
                            self.variables[current_variable].append(line)
            fp.close()
            self.number_of_variables = len(self.variables.keys())

            curr = 0
            prev = 0

            for variable in self.variables.keys():
                curr = len(self.variables[variable])

                # Pierwszy obrót petli, czyli "prev = 0"
                if prev == 0:
                    prev = curr
                else:
                    if curr == prev:
                        prev = curr
                    else:
                        # Błąd, zwracane zero
                        self.number_of_hosts = 0

            self.number_of_hosts = curr
        except FileNotFoundError:
            print("File Not Found: " + file)

    def get_variable_collection(self, host):
        collection = {}

        for v in self.variables.keys():
            collection[v] = self.variables[v][host]

        return collection
