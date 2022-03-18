"""
A Dashboard created with python using the dash library.
I use it to visualize the outcomes of my Scheduling-Algorithm-Simulator.
"""

__author__ = "Anton Roesler"
__email__ = "anton.roesler@stud.fra-uas.de"

import os
import dash
#import dash_html_components as html
from dash import html
#import dash_core_components as dcc
from dash import dcc
import plotly.figure_factory as ff
#import dash_table
from dash import dash_table
import flask
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from Scheduler import Scheduler
from ProcessList import ProcessListAdministration

# VARIABLES
filename = 'processes.csv'  # the filename or path to the csv file with the processes on it
algorithm_titles = [
    "First Come First Served",
    "Shortest Job First",
    "Highest Response Ratio Next",
    "Shortest Remaining Time First",
    "Longest Remaining Time First",
    "Round Robin",
    "Evolutionary Algorithm"
]
num_clicks = 0
quantum = 3  # Used for the Round Robin Algortihm


class Namer:
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
app = dash.Dash(__name__, external_stylesheets=[BS])
server = app.server  # This is the Flask app for deploy on Heroku

title = html.Div(
    html.H1(children="Visualization of Scheduling Algorithms", style={'fontSize': 30, 'font-family': 'Gidole'}))

# A Dropdown with links to my social media.
bar_drop = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem(
                    "See the Code", href="https://github.com/antonroesler/ProcessScheduler"
        ),
        dbc.DropdownMenuItem(
                    "My Linked-in", href="https://www.linkedin.com/in/antonroesler/"
        ),
    ],
    label='More',
    style={'padding': 20}
)
# The Navbar is the header with title and links to my github and linked-in.
navbar = dbc.NavbarSimple(children=[
    dbc.Row(
        [
            dbc.Col(
                [
                    title
                ], align='start'

            ),
            dbc.Col(
                [
                    bar_drop
                ], align='end'
            )
        ]
    )
    ],)

# The Dropdown Menu to choose an algorithm.
dropdown = dcc.Dropdown(
    id='demo-dropdown',
    options=[
        {'label': algorithm_titles[0], 'value': 0},
        {'label': algorithm_titles[1], 'value': 1},
        {'label': algorithm_titles[2], 'value': 2},
        {'label': algorithm_titles[3], 'value': 3},
        {'label': algorithm_titles[4], 'value': 4},
        {'label': algorithm_titles[5], 'value': 5},
        {'label': algorithm_titles[6], 'value': 6}
    ],
    style={'fontSize': 19, 'font-family': 'Gidole'},
    searchable=False,
    placeholder="Select an Algorithm",

)

chart = html.Div(id='chart')  # This is the chart object!

# An Input field to let the user add his own processes
add_process_field = dbc.InputGroup(
    [
        dbc.InputGroupAddon(dbc.Button("Add", id="add-button", color="success"),
                            addon_type="prepend"),
        dbc.Input(placeholder="Name", type="text", id="name-input"),
        dbc.Input(placeholder="Duration", type="number", id="duration-input"),
        dbc.Input(placeholder="Arrival Time", type="number", id="arrival-input"),
    ],
)

add_text = html.Div("Here you can add or modify as many processes as you want:", style={'padding': 20})

# A Button to clear the process list
clear_button = dbc.Button("Clear", id='clear-button', color='warning')

# The Card Shows Statistical information
stat_card = dbc.Card(
    [
        dbc.CardHeader(
            html.H4("STATS")
        ),
        dbc.CardBody(
            [
                dbc.Table(
                    html.Tbody(
                        [
                            html.Tr([html.Td("Waiting Mean"), html.Td(12, id='w-mean')]),
                            html.Tr([html.Td("Turnaround Mean"), html.Td(13, id='t-mean')]),
                            html.Tr([html.Td("Waiting Median"), html.Td(140, id='w-median')]),
                            html.Tr([html.Td("Turnaround Median"), html.Td(111, id='t-median')])
                        ]
                    )
                )
            ]
        )
    ],
)

# Slider to adjust the quantum of Round Robin algorithm
slider = dcc.Slider(
    id='slider',
    min=1,
    max=20,
    step=1,
    value=3
)

slider_card = dbc.Card(
    [
        dbc.CardHeader(
            html.H4("Round Robin Quantum")
        ),
        dbc.CardBody(
            [
                html.Div("Here you can adjust the length of the quantum or time slice that is used fot the Round"
                         " Robin scheduling."),
                slider,
                html.Div(id='slider-text')
            ]
        )
    ]
)

# The Compare Button opens a Modal where one can see a bar chart with all the stats compared
compare = dbc.Button("Compare Algorithms", id='compare', color='info', block=True)

namer.set("quantum", 3)  # Default value of the quantum is 3. Changes as the slider changes.


# The Compare Modal shows a bar chart to compare the stats of all of the Algorithms
def get_comparison():
    """Returns Data to compare all the stats of the algorithm. By running every Algorithm in a separate Scheduler."""
    c_scheduler = Scheduler(process_list)  # A new separate Scheduler to run the comparison in.
    stat_names = [  # Names of the Stats for the x-axis.
        "Waiting Time Mean",
        "Waiting Time Median",
        "Turnaround Time Mean",
        "Turnaround Time Median",
        ]
    c_scheduler.set_quantum(namer.get("quantum"))  # Set quantum for Round Robin to right value before run simulation.
    stats = c_scheduler.run_all()  # Get the stats.
    fig = go.Figure()  # Create a figure
    fcfs = [f'{x} - {algorithm_titles[0]}' for x in stats["fcfs"]]
    sjf = [f'{x} - {algorithm_titles[1]}' for x in stats["sjf"]]
    hrrn = [f'{x} - {algorithm_titles[2]}' for x in stats["hrrn"]]
    srtf = [f'{x} - {algorithm_titles[3]}' for x in stats["srtf"]]
    lrtf = [f'{x} - {algorithm_titles[4]}' for x in stats["lrtf"]]
    rr = [f'{x} - {algorithm_titles[5]}' for x in stats["rr"]]
    ea = [f'{x} - {algorithm_titles[6]}' for x in stats["ea"]]
    fig.add_trace(go.Bar(x=stat_names, y=stats['fcfs'], name="First Come First Served", text=fcfs, hoverinfo='text'))
    fig.add_trace(go.Bar(x=stat_names, y=stats['sjf'], name="Shortest Job First", text=sjf, hoverinfo='text'))
    fig.add_trace(go.Bar(x=stat_names, y=stats['hrrn'], name="Highest Response Ratio Next", text=hrrn, hoverinfo='text'))
    fig.add_trace(go.Bar(x=stat_names, y=stats['srtf'], name="Shortest Remaining Time First", text=srtf, hoverinfo='text'))
    fig.add_trace(go.Bar(x=stat_names, y=stats['lrtf'], name="Longest Remaining Time First", text=lrtf, hoverinfo='text'))
    fig.add_trace(go.Bar(x=stat_names, y=stats['rr'], name="Round Robin", text=rr, hoverinfo='text'))
    fig.add_trace(go.Bar(x=stat_names, y=stats['ea'], name="Evolutionary Algorithm", text=rr, hoverinfo='text'))
    return fig


compare_modal = dbc.Modal(  # A modal that shows a bar chart to compare the Algorithms.
    [
        dbc.ModalHeader("COMPARE HOW GOOD THE DIFFERENT ALGORITHMS ARE"),
        dbc.ModalBody(
            [
                dcc.Graph(id="bar-chart", figure=get_comparison())
            ]
        ),
        dbc.ModalFooter(
            dbc.Button("Close", id="compare-close", className="ml-auto")
        )
    ],
    id='compare-modal',
    size='xl'
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
        dbc.Row(add_text),
        dbc.Row(
            [
                dbc.Col(
                    [
                        add_process_field
                    ], width=10
                ),
                dbc.Col(
                    clear_button
                )
            ], style={'padding': 30}

        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        stat_card,

                    ],
                    width=6,

                ),
                dbc.Col(
                    [
                        dbc.Row(slider_card),
                        dbc.Row(compare, style={'padding': 20})

                    ]
                )
            ],
            justify='center'
        ),
        compare_modal
    ], style={'padding': 20}
)


@app.callback(
    Output('chart', 'children'),
    [Input('demo-dropdown', 'value'), Input("add-button", "n_clicks"),
     Input("clear-button", "n_clicks"), Input('slider-text', 'children')])
def update_output(value, x, y, z):
    """This is to updated the main gantt chart if the user changes the value of the dropdown menu."""
    if value == 1:  # For the clicked value the Algorithm will be executed.
        a_title = algorithm_titles[1]
        scheduler.non_preemtive_algorithms(sjf=True)
    elif value == 2:
        a_title = algorithm_titles[2]
        scheduler.non_preemtive_algorithms(hrrn=True)
    elif value == 3:
        a_title = algorithm_titles[3]
        scheduler.remaining_time_first()
    elif value == 4:
        a_title = algorithm_titles[4]
        scheduler.remaining_time_first(longest=True)
    elif value == 5:
        a_title = algorithm_titles[5]
        scheduler.round_robin()
    elif value == 6:
        a_title = algorithm_titles[6]
        scheduler.ea()
    else:
        a_title = algorithm_titles[0]
        scheduler.non_preemtive_algorithms()
    data = scheduler.data_plotly_formatted()  # The data is what was simulated by the Scheduler.
    data = sorted(data, key=lambda i: i['Task'])
    fig = ff.create_gantt(data, group_tasks=True, showgrid_x=True, title=a_title + " visualized:",
                          colors=scheduler.get_colors(), index_col='Task', show_colorbar=True)
    fig.layout.xaxis.tickformat = "%Mm %Ss"  # Show minutes and Seconds as '00m 00s'
    graph = dcc.Graph(id="graph", figure=fig)  # Create the graph.

    return graph


# CALLBACKS FOR THE ADD-A-NEW-PROCESS INPUT FIELD GROUP
@app.callback(
    Output("add-button", "children"),  #
    [Input("add-button", "n_clicks")]
)
def add_button_click(n, num_clicks=num_clicks):
    """This is the call back function for the Add button. What it does, is take the values from the fields, which are
    stored in the variables by their own call backs. And if everything needed is there, a new Process will be created
    inside the process list with te input given by the user."""
    if n is None:
        n = 0
    if n-num_clicks == 0:
        pass
    elif namer.get('name') is None or namer.get('duration') is None or namer.get('arrival') is None:
        pass
    else:
        exists = False
        for p in process_list.processes:  # DONT Use get_process_list -> it returns a deepcopy.
            # First we see if a process name already exists inside the list, if so: its values will get adjusted:
            if p.name == namer.get('name'):  # User inputs are stored in the namer.
                process_list.remove(p)
                process_list.add(namer.get('name'), namer.get('duration'), namer.get('arrival'))
                exists = True
                break
        if not exists:  # Only if a process name does not already exists in the list ir will be added.
            process_list.add(namer.get('name'), namer.get('duration'), namer.get('arrival'))


# CALLBACKS FOR THE USER INPUTS
# User inputs will be saved in the Namer!
@app.callback(
    Output("name-input", "value"),  #
    [Input("name-input", "value")]
)
def update_name(value):
    namer.set('name', value)


@app.callback(
    Output("duration-input", "value"),  #
    [Input("duration-input", "value")]
)
def update_duration(value):
    namer.set('duration', value)


@app.callback(
    Output("arrival-input", "value"),  #
    [Input("arrival-input", "value")]
)
def update_arrival(value):
    namer.set('arrival', value)


@app.callback(
    Output("clear-button", "children"),  #
    [Input("clear-button", "n_clicks")]
)
def clear_processlist(n):
    if n:
        process_list.clear()


# CALL BACKS FOR THE INFO STATS
@app.callback(
    Output("w-mean", "children"),
    [Input('chart', 'children')]
)
def updated_w_mean(value):
    return scheduler.stats[0]


@app.callback(
    Output("t-mean", "children"),
    [Input('chart', 'children')]
)
def update_t_mean(value):
    return scheduler.stats[2]


@app.callback(
    Output("w-median", "children"),
    [Input('chart', 'children')]
)
def update_w_median(value):
    return scheduler.stats[1]


@app.callback(
    Output("t-median", "children"),
    [Input('chart', 'children')]
)
def update_w_median(value):
    return scheduler.stats[3]


# SLIDER CALL BACK
@app.callback(
    Output('slider-text', 'children'),
    [Input('slider', 'value')])
def update_slider(value):
    namer.set("quantum", value)
    scheduler.set_quantum(value)
    return f"Value: {value}"


# COMPARE CALL BACK
@app.callback(
    Output('compare-modal', 'is_open'),
    [Input('compare', 'n_clicks'), Input('compare-close', 'n_clicks')],
    [State('compare-modal', 'is_open')])
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output('bar-chart', 'figure'),  # Update the Bar Chart Figure.
    [Input('compare', 'n_clicks')])
def update_modal(is_open):
    return get_comparison()


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
