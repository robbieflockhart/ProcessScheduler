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
        {'label': 'First come first served', 'value': 1},
        {'label': 'Shortest Job first', 'value': 2},
        {'label': 'Highest response ratio next', 'value': 3},
        {'label': 'Shortest remaining time first', 'value': 4},
        {'label': 'Longest remaining time first', 'value': 5},
        {'label': 'Round Robin', 'value': 6}
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
    if value == 2:
        title = "Shortest Job First"
        scheduler.non_preemtive_algorithms(sjf=True)
    else:
        title = "First Come First Served"
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
