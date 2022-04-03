"""The Process List contains the List of Processes. It contains all functions needed to add processes to the list,
clear the list etc. The Scheduler grabs the list from here."""

__author__ = "Anton Roesler"
__email__ = "anton.roesler@stud.fra-uas.de"

from Process import Process
from copy import deepcopy


class ProcessListAdministration:
    def __init__(self):
        self.processes = []

    def add(self, name: str, duration: int, arrival_time: int):
        """Builds a new process object from given args. This new process is added to the process list."""
        self.processes.append(Process(name, duration, arrival_time))

    def add_process(self, process: Process):
        """Adds a given process to the process list"""
        self.processes.append(process)

    def remove(self, process: Process):
        """Removes a given process."""
        self.processes.remove(process)

    def clear(self):
        """Empties the process list"""
        self.processes = []

    def get_process_list(self):
        """Returns a deepcopy of the process list."""
        if len(self.processes) == 0:
            return [Process('null', 1, 0)]  # if the list is completely empty a pseudo process will be returned.
        return deepcopy(self.processes)

    def read_csv(self, filepath):
        """Reads a csv file formatted as 'name, duration, arrival_time' and adds every line as a new process to the
        process list."""


        file = open("processes5.csv", 'r')
        file.readline()  # Skip the first row inside csv file.
        #file = [['a',11,0],['b',17,0],['c',3,0],['x',19,57]]
        for line in file:
            if not line:
                break  # if the row is empty, the last row is reached and the for loop is done.
            line = line.split(',')  # Separate row into its 3 parts, at the comma.
            if len(line) >= 3:  # Only precede if all the arguments are available.
                self.processes.append(Process(line[0], int(line[1]), int(line[2])))  # Add as a new process to the list.
        file.close()

