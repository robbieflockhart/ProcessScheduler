# ProcessScheduler
A Visualization of Scheduling Algorithms using pure python with dash and plotly

Here is a five minute demo video on my Youtube Channel: https://youtu.be/5KJTk0CCvX0

The Scheduler.py Class is where all the Algorithms are implemented. The ProcessList can read a csv file with Processes in the form of 'name,duration,arrival' in it, or one can simply add Processes by hand. This customizable ProcessList can then be scheduled by any of the six algorithms ("First Come First Served", "Shortest Job First", "Highest Response Ratio Next", "Shortest Remaining Time First", "Longest Remaining Time First", "Round Robin"). The data can then be pulled from the Scheduler and plotted. 

The app.py is my version of a Dashboard for the visualization. My goal was a nicely layouted and interaktiv app. The User can choose any of the algorithms to see the example Processes visualized. The User can modify or add as many new Processes to chart as he wants. The dashboard shows stats as 'mean waiting time' etc. for every Algorithm, calculated for the current Processes. Those stats can be compared in a Bar Chart. 
