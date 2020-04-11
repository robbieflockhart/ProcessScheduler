"""
A Dashboard created with python using the dash library.
It used to visualize the outcomes of my Scheduling-Algorithm-Simulator.
"""

__author__ = "Anton Roesler"
__email__ = "anton.roesler@stud.fra-uas.de"

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.figure_factory as ff
import dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from Scheduler import Scheduler
from ProcessList import ProcessListAdministration

# VARIABLES
filename = 'processes.csv'  # the filename or path to the csv file with the processes on it
algorithm_titles = [
    "Frist Come First Served",
    "Shortest Job First",
    "Highest Response Ratio Next",
    "Shortest Remaining Time First",
    "Longest Remaining Time First",
    "Round Robin"
]
# SIMULATOR
process_list = ProcessListAdministration()
process_list.read_csv(filename)
scheduler = Scheduler(process_list)

# Dash
app = dash.Dash()

title = html.Div(
    html.H1(children="Visualization of Scheduling Algorithms", style={'fontSize': 30, 'font-family': 'Gidole'}))

dropdown = dcc.Dropdown(
    id='demo-dropdown',
    options=[
        {'label': algorithm_titles[0], 'value': 0},
        {'label': algorithm_titles[1], 'value': 1},
        {'label': algorithm_titles[2], 'value': 2},
        {'label': algorithm_titles[3], 'value': 3},
        {'label': algorithm_titles[4], 'value': 4},
        {'label': algorithm_titles[5], 'value': 5}
    ],
    style={'fontSize': 19, 'font-family': 'Gidole'},
    searchable=False,
    placeholder="Select an Algorithm",
)

chart = html.Div(id='chart')

app.layout = html.Div(
    [
        dbc.Row(
            title

        ),
        dbc.Row(
            dropdown
        ),
        dbc.Row(
            chart
        )
    ]
)

@app.callback(
    dash.dependencies.Output('chart', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    """This is to updated the main gantt chart if the user changes the value of the dropdown menu."""
    if value == 1:
        title = algorithm_titles[1]
        scheduler.non_preemtive_algorithms(sjf=True)
    elif value == 2:
        title = algorithm_titles[2]
        scheduler.non_preemtive_algorithms(hrrn=True)
    elif value == 3:
        title = algorithm_titles[3]
        scheduler.remaining_time_first()
    elif value == 4:
        title = algorithm_titles[4]
        scheduler.remaining_time_first(longest=True)
    elif value == 5:
        title = algorithm_titles[5]
        scheduler.round_robin()
    else:
        title = algorithm_titles[0]
        scheduler.non_preemtive_algorithms()
    data = scheduler.data_plotly_formatted()
    data = sorted(data, key=lambda i: i['Task'])
    fig = ff.create_gantt(data, group_tasks=True, showgrid_x=True, title=title + " visualized:",
                          index_col='Task', show_colorbar=True)
    fig.layout.xaxis.tickformat = "%Mm %Ss"
    graph = dcc.Graph(id="graph", figure=fig)
    return graph

if __name__ == '__main__':
    app.run_server(debug=True)
