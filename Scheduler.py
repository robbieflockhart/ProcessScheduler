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

    # GENERAL FUNCTIONS
    def reset(self):
        self.passed_time = 0
        self.data = []
        self.update_process_list()

    def update_process_list(self):
        """Sets the process list."""
        self.process_list = self.process_list_admin.get_process_list()

    #  SCHEDULING ALGORITHMS
    def non_preemtive_algorithms(self, sjf=False, hrrn=False):
        """
        This is the Algorithm for:
         - First Come First Served
         - Shortest Job First
         - Highest Response Ratio Next
        The Default is set FCFS. SJF or HRRN can be used by setting the sjf or hrrn argument to True.
        """
        self.reset()
        while not self.check_if_done():  # check if there are still unfinished processes inside the process list.

            possible_jobs = self.get_competing_processes()  # All process that are competing to be processed.
            if sjf:  # If the user wants to use SJF:
                possible_jobs.sort(key=lambda x: x.remaining_time)  # Jobs get sorted by remaining time.
            elif hrrn:  # If the user wants to use HRRN:
                possible_jobs.sort(key=lambda x: x.get_response_ratio(passed_time=self.passed_time))  # Jobs get sorted by response ratio.
            else:  # Default is FCFS:
                possible_jobs.sort(key=lambda x: x.arrival_time)  # Jobs get sorted by arrival time.

            self.process(possible_jobs[0])  # The first process in the list is the one to be done.

    def remaining_time_first(self, longest=False):
        """
        This can either be Longest or Shortest remaining time first. The default is Shortest, by setting longest to true
        it will switch to the Scheduling Algorithm Longest remaining time first.
        The longest/shortest job starts first, if a longer/shorter job comes in, the longer/shorter one will be finished
        first.
         """
        self.reset()
        latest_job = None  # The latest job is always the job that was processed in the last step - at beginning: None.
        while not self.check_if_done():  # Check if there are still jobs not done.
            possible_jobs = self.get_competing_processes()  # get the list of competing jobs at this time point.

            # Default is longest=False - if longest=True, the list will be sorted reverse!
            possible_jobs.sort(key=lambda x: x.remaining_time, reverse=longest)
            # Reverse means descending - so the longest remaining time will be at the first position in list.
            # The jobs with the shortest/longest remaining time left, is the first one in list.
            current_job = possible_jobs[0]

            self.process_one_step(current_job, latest_job)  # The job is processed here.

            latest_job = current_job  # Now the job that was just processed is the (new) latest job.

        # The last process's data doesnt get added to the data table inside the functions, because this happens in the
        # next step. And there is no next step for the last one, So it happens here:
        self.add_data(latest_job.name, latest_job.row_start_time, latest_job.row)

    def round_robin(self):
        """Round Robin Scheduling Algorithm"""
        self.reset()
        quantum = 3  # The length of the time slice for every job ToDo: this should be adjustable by the user.
        already_processed = []
        while not self.check_if_done():  # Check if there are still jobs not done.
            possible_jobs = self.get_competing_processes()  # Get the list of competing jobs at this time point.
            possible_jobs.sort(key=lambda x: x.arrival_time)  # Sort by arrival time.
            current_job = None
            for i in range(len(possible_jobs)):       # Check for every possible job
                current_job = possible_jobs[i]
                if current_job in already_processed:  # if this jobs was already processed
                    current_job = None  # if it was, current jib is set back to none.
                else:  # if it wasn't then break out of loop an continue with this job as the current one.
                    break
            if not current_job:  # If every possible job was already processed then start with the beginning and reset:
                current_job = possible_jobs[0]
                already_processed = []  # Empty the list to start over again.

            duration = quantum  # If time gets changed, quantum should stay the same for next iteration.
            if current_job.remaining_time < duration:  # If the jobs remaining time is less than the quantum
                duration = current_job.remaining_time  # the time slice for the processing gets shortened to that time.

            self.add_data(current_job.name, self.passed_time, duration)  # Add the data to the data table
            self.passed_time += duration  # Increase the passed time
            current_job.process(duration, self.passed_time)  # Adjust the parameter inside the job itself.
            already_processed.append(current_job)  # Ad the job to the list of processed ones.

    # SCHEDULING ALGORITHM SUPPORTING FUNCTIONS
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
            start = self.start + datetime.timedelta(seconds=entry[1])
            finish = self.start + datetime.timedelta(seconds=entry[2])
            plotly_chart_data.append(dict(Task=name, Start=start, Finish=finish,
                                          Description=f'Task: {name} Duration: {finish-start}'))
        return plotly_chart_data

    def process_one_step(self, process, latest_job):
        """This is used for shortest and longest remaining time only (preemtives)."""
        if process != latest_job and latest_job is not None:
            # This is the case if the process that will be processed in this step is a different from the previous one.
            # Then the data from the previous one need to be added to the data table.
            self.add_data(latest_job.name, latest_job.row_start_time, latest_job.row,)
            latest_job.row_start_time = None
            latest_job.row = 0  # And the previous job's row data  goes back to 0.

        if process.starting_time is None:
            # If this is the first step for the current process, the starting time is set.
            process.starting_time = self.passed_time

        if process.row_start_time is None:
            # If this is the first step in the current row of the current process, its row starting time is set.
            process.row_start_time = self.passed_time

        # With preemtive algorithms only one step at a time is possible
        process.row += 1  # Increase jobs row by one.
        process.remaining_time -= 1  # The remaining time is now one time unit shorter.
        self.passed_time += 1  # And the simulations passed time is also by one time unit increased.

        if process.finished():
            process.end_time = self.passed_time

    # Create Colors for Gantt Chart
    def get_colors(self):
        self.update_process_list()
        colors = [
            'rgb(181, 18, 80)',
            'rgb(219, 202, 13)',
            'rgb(23, 18, 181)',
            'rgb(62, 161, 16)',
            'rgb(150, 35, 35)',
            'rgb(18, 127, 181)',
            'rgb(227, 112, 18)',
            'rgb(110, 18, 181)',
            'rgb(33, 219, 185)',
            'rgb(181, 18, 170)',
            'rgb(33, 219, 92)'
        ]
        color_dict = {}
        i = 0
        for process in self.process_list:
            color_dict[process.name] = colors[i % len(colors)]
            i += 1
        return color_dict
