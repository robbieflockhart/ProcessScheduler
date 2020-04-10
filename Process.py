"""Processes are implemented as objects. This class represents theses Processes as Objects. They include all functions
for the calculation of stats."""

__author__ = "Anton Roesler"
__email__ = "anton.roesler@stud.fra-uas.de"

class Process:
    def __init__(self, name: str, duration: int, arrival_time: int):
        self.name = name
        self.duration = duration
        self.arrival_time = arrival_time
        self.remaining_time = duration  # Number of time units left until a process is done, starts with the duration.
        self.starting_time = None  # Number of time units when the process starts, with 0 being the start of simulation.
        self.end_time = None  # Number of time units when the process ends, with 0 being the start of the simulation.
        self.row = 0  # A Measure needed for lrtf, indicates how many time units the process was processed continuously.
        self.row_start_time = None  # Indicates at what time unit the current row started.

    def finished(self)->bool:
        """A quick check if a process is finished. The remaining time indicates how many time units are left until the
        process is done. That means a process with a remaining time of 0 is considered finished."""
        if self.remaining_time <= 0:
            return True
        return False