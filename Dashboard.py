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
num_clicks = 0

class Namer():
    """A class to store variables and their values in (in for of a dict. I used it for storing user inputs."""
    def __init__(self):
        self.names = dict()

    def set(self, name, value):
        """Adds a new entry or updates an existing one in the dict."""
        self.names[name] = value

    def get(self, name):
        """Outputs a value to a given key. Or None if there is no key with that name."""
        return self.names.get(name)

namer = Namer()

# SIMULATOR
process_list = ProcessListAdministration()
process_list.read_csv(filename)
scheduler = Scheduler(process_list)

# Dash
BS = 'https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/flatly/bootstrap.min.css'
app = dash.Dash(external_stylesheets=[BS])

title = html.Div(
    html.H1(children="Visualization of Scheduling Algorithms", style={'fontSize': 30, 'font-family': 'Gidole'}))

navbar = dbc.NavbarSimple(children=[title],fluid=True,sticky='top')

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

add_process_field = dbc.InputGroup(
    [
        dbc.InputGroupAddon(dbc.Button("Add", id="add-button", color="success"),
                            addon_type="prepend"),
        dbc.Input(placeholder="Name", type="text", id="name-input"),
        dbc.Input(placeholder="Duration", type="number", id="duration-input"),
        dbc.Input(placeholder="Arrival Time", type="number", id="arrival-input"),
    ],
    style={'padding': 15}
)

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                navbar
            )

        ),
        dbc.Row(
            dbc.Col(
                dropdown
            ), style={'padding': 15}
        ),
        dbc.Row(
            dbc.Col(
                chart
            )
        ),
        dbc.Row(
            dbc.Col(
                add_process_field
            )

        )
    ]
)

@app.callback(
    Output('chart', 'children'),
    [Input('demo-dropdown', 'value'), Input("add-button", "n_clicks")])
def update_output(value, x):
    """This is to updated the main gantt chart if the user changes the value of the dropdown menu."""
    if value == 1:  # For the clicked value the Algorithm will be executed.
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
    data = scheduler.data_plotly_formatted()  # The data is what was simulated by the Scheduler.
    data = sorted(data, key=lambda i: i['Task'])
    fig = ff.create_gantt(data, group_tasks=True, showgrid_x=True, title=title + " visualized:",
                          colors=scheduler.get_colors(), index_col='Task', show_colorbar=True)
    fig.layout.xaxis.tickformat = "%Mm %Ss"  # Show minutes and Seconds as '00m 00s'
    graph = dcc.Graph(id="graph", figure=fig)  # Create the graph.
    return graph

# CALLBACKS FOR THE ADD-A-NEW-PROCESS INPUT FIELD GROUP
@app.callback(
    Output("add-button", None),
    [Input("add-button", "n_clicks")]
)
def on_button_click(n, num_clicks=num_clicks):
    """This is the call back function for the Add button. What it does, is take the values from the fields, which are
    stored in the variables by their own call backs. And if everything needed is there, a new Process will be created
    inside the process list with te input given by the user."""
    if n is None:
        n = 0
    if n-num_clicks is 0:
        pass
    elif namer.get('name') is None or namer.get('duration') is None or namer.get('arrival') is None:
        print("hi")
        pass
    else:
        exists = False
        for p in process_list.processes:  # DONT Use get_process_list -> it returns a deepcopy hahah took me a while.
            # First we see if a process name already exists inside the list, if so: its values will get adjusted:
            if p.name == namer.get('name'):  # User inputs are stored in the namer.
                process_list.remove(p)
                process_list.add(namer.get('name'), namer.get('duration'), namer.get('arrival'))
                exists = True
                break
        if not exists:  # Only if a process name does not already exists in the list ir will be added.
            process_list.add(namer.get('name'), namer.get('duration'), namer.get('arrival'))



@app.callback(
    Output("name-input", None),
    [Input("name-input", "value")]
)
def update_name(value):
    namer.set('name', value)


@app.callback(
    Output("duration-input", None),
    [Input("duration-input", "value")]
)
def update_name(value):
    namer.set('duration', value)


@app.callback(
    Output("arrival-input", None),
    [Input("arrival-input", "value")]
)
def update_name(value):
    namer.set('arrival', value)


if __name__ == '__main__':
    app.run_server(debug=True)
