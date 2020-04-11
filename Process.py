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

    def finished(self) -> bool:
        """A quick check if a process is finished. The remaining time indicates how many time units are left until the
        process is done. That means a process with a remaining time of 0 is considered finished."""
        if self.remaining_time <= 0:
            return True
        return False

    def get_response_ratio(self, passed_time: int) -> float:
        """Calculates and returns the response ratio."""
        waiting_time = passed_time - self.arrival_time
        response_ratio = (waiting_time+self.duration)/self.duration
        return response_ratio

    def process(self, time_units: int, current_time: int):
        """This functions simulates that the process gets processed 'time_units' time units. Everything that happens
        is, that the remaining_time gets shortend by int 'time_units'."""
        self.remaining_time -= time_units

        if self.remaining_time <= 0:  # If the process is finished with this step, the end time gets set.
            self.end_time = current_time

    def get_waiting_time(self):
        """The total waiting time is the total turnaround time minus the duration."""
        return self.end_time - self.arrival_time - self.duration

    def get_turnaround_time(self):
        """The total turnaround time is the end time minus the start time."""
        return self.end_time - self.arrival_time

    def info(self):
        print(f'{self}\n{self.name}\nstart: {self.starting_time}\nend: {self.end_time}\nrem: {self.remaining_time}'
              f'\ndur: {self.duration}\nwait:{self.get_waiting_time()} ')
