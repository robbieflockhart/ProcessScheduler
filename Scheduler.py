"""
All simulations run in here.
Important information: The time inside the Simulation is simply expressed by integer values. The Simulation starts at
time unit 0. If a process has a arrival time of 42, it will show up inside the Simulation as soon as passed time has
reached a value of 42. For the plotly gantt chart a time has to have a proper datetime. For that I chose to set the
start time as 2020-01-01 00:00:00 - it doesnt really matter. A simulation's time unit is transformed into 1 second
for the gantt chart. It can be changed to milliseconds, minutes or whatever in line ToDo
"""

__author__ = "Anton Roesler"
__email__ = "anton.roesler@stud.fra-uas.de"

from ProcessList import ProcessListAdministration
from Process import Process
from typing import List
import datetime


class Scheduler:
    def __init__(self, process_list_admin: ProcessListAdministration):
        self.process_list_admin = process_list_admin
        self.process_list: List[Process] = None
        self.passed_time = 0  # Number of time units passed since the start time, only integer values.
        self.data = []  # Data for the diagram

        # The start time is considered 0.
        self.start = datetime.datetime.fromisoformat("2020-01-01 00:00:00")  # other option: datetime.datetime.now()

    def reset(self):
        self.passed_time = 0
        self.data = []
        self.update_process_list()

    def update_process_list(self):
        """Sets the process list."""
        self.process_list = self.process_list_admin.get_process_list()

    #  SCHEDULING ALGORITHMS
    def first_come_first_served(self):
        """In the order they come in. Ones a job started, it will be finished."""
        self.reset()
        while not self.check_if_done():  # check if there are still unfinished processes inside the process list.

            possible_jobs = self.get_competing_processes()  # All process that are competing to be processed.
            possible_jobs.sort(key=lambda x: x.arrival_time)  # jobs get sorted after come in time.

            self.process(possible_jobs[0])  # the first process in the list is the one to be done



    def shortest_job_first(self):
        """Shortest job first, if a job comes in, it'll be put in the right place, once a job started it'll be done."""
        self.reset()
        while not self.check_if_done():  # check if there are still jobs not done
            possible_jobs = self.get_competing_processes()
            possible_jobs.sort(key=lambda x: x.duration)

            self.process(possible_jobs[0])  # the first process in the list is the one to be done



    def highest_response_ration_next(self):
        """Shortest job first, if a job comes in, it'll be put in the right place, once a job started it'll be done."""
        self.reset()
        while not self.check_if_done():  # check if there are still jobs not done
            possible_jobs = self.get_competing_processes()
            possible_jobs.sort(key=lambda x: x.get_response_ratio())

            self.process(possible_jobs[0])  # the first process in the list is the one to be done



    # SUPPORTING FUNCTIONS
    def get_competing_processes(self) -> List[Process]:
        """Returns a list of all jobs that already exist at this time (passed_time) and are not already finished."""
        competing_processes: List[Process] = []
        for process in self.process_list:
            if process.arrival_time - self.passed_time <= 0 and not process.finished():
                competing_processes.append(process)  # only jobs that exist and are not finished.
        if len(competing_processes) > 0:  # Return list if there is at least one process in th list.
            return competing_processes
        else:  # If there is no job waiting to be processed, the passed time will be increased by one and the
            # function gets called again
            self.passed_time += 1
            return self.get_competing_processes()

    def check_if_done(self) -> bool:
        """Checks if every process in process-list is finished, returns True or False."""
        for process in self.process_list:
            if not process.finished():
                return False
        return True

    def process(self, process: Process):
        """This function does the processing part, which is the same for fcfs, sjf, hrrn (all non-preemtives)."""
        duration = process.duration
        self.add_data(process.name, self.passed_time, duration)
        process.starting_time = self.passed_time
        # Since this is only used for non-preemptives algorithms the whole process will be finished
        self.passed_time += duration  # by increasing the passed time by the process's duration.
        process.process(duration, self.passed_time)  # The process itself need to be updated.

    def add_data(self, name: str, start: int, duration: int):
        """Every piece that gets processed is saved as an entry in the data table."""
        finish = start+duration
        self.data.append([name, start, finish])

    def data_plotly_formatted(self) -> List:
        """Turns the data list into a list of dicts that can be used for the plotly/dash gantt chart."""
        plotly_chart_data = []
        for entry in self.data:
            name = entry[0]
            start = entry[1]
            finish = entry[2]
            plotly_chart_data.append(dict(Task=name, Start=start, Finish=finish,
                              Description=f'Task: {name} Duration: {finish-start}'))
        return plotly_chart_data
