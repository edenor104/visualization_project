import os
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from app import app
import os

folder_path = os.getcwd() + r"\Data\Raw Data\Data"

# Get list of participant folders
participant_folders = sorted(os.listdir(folder_path))

def get_key_from_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None  # If the value is not found in the dictionary

# Define function to plot facets
def plot_facets(data, parameter_string):
    converstion_selection = {'Completion Time [s]': 'completion_time','Success Rate': 'success_maze'}
    parameter = converstion_selection[parameter_string]

    # Create a new column for the desired x-axis values (0 to 3 for each condition)
    data['x_axis'] = data.groupby('condition').cumcount()

    # Get unique conditions and their original colors
    conditions = data['condition'].unique()
    condition_conversion = {'Multisensory': 'all', 'Visual Only': 'visual_only', 'Auditory Only':'audio_only', 'Invisible':'invisible', 'Partial Visual Clash':'contra_visual',
     'Partial Audio Clash':'contra_audio', 'Full Visual Clash':'const_contra_visual', 'Full Audio Clash':'const_contra_audio2'}
    fig = make_subplots(rows=2, cols=4, shared_xaxes=True, shared_yaxes=True,
                        subplot_titles=[f"Condition: {get_key_from_value(condition_conversion, condition)}" for condition in conditions],
                        x_title='Time / Order of Performance [n]', y_title=parameter_string)

    # Iterate over each subplot and update layout properties
    for i in range(1, 9):  # There are 8 subplots in total (2 rows * 4 cols)
        fig.update_xaxes(gridcolor='#474747', gridwidth=3, row=i // 4 + 1, col=i % 4 + 1)
        fig.update_yaxes(gridcolor='#474747', gridwidth=3, row=i // 4 + 1, col=i % 4 + 1)

    # Plot line plot for each condition with original colors
    for i, condition in enumerate(conditions):
        row = i // 4 + 1
        col = i % 4 + 1
        group = data[data['condition'] == condition]

        # Plot line plot
        fig.add_trace(go.Scatter(x=group['x_axis'], y=group[parameter], mode='lines+markers',
                                     name=condition, marker=dict(color="#D5D5D5")), row=row, col=col)
        fig.update_traces(line=dict(width=4))
        if parameter_string == 'Completion Time [s]':
            # Add horizontal line at y = 20
            fig.add_shape(type="line", x0=min(group['x_axis']), y0=20, x1=max(group['x_axis']), y1=20,
                          line=dict(color="#D5D5D5", width=1, dash="dash"), row=row, col=col)
        fig.update_layout(plot_bgcolor='black',  # Set background color to black
                          paper_bgcolor='black',  # Set plot's paper background color to black
                          font=dict(color='white'),  # Set font color to white for better visibility
                          xaxis=dict(
                              gridcolor='#474747',  # Set x-axis grid color to red
                              gridwidth=3),  # Set x-axis grid width to 2),
                          yaxis=dict(
                              gridcolor='#474747',  # Set y-axis grid color to blue
                              gridwidth=3),  # Set x-axis grid width to 2
                          )
        fig.update_layout(
            xaxis=dict(linecolor='#474747'),  # Set x-axis line color to red
            yaxis=dict(linecolor='#474747')  # Set y-axis line color to blue
        )

    # Update layout
    fig.update_layout(showlegend=False)

    return fig


loading_card3 = dbc.Card([
    html.Div(
        [
            html.H6('Participant selection', className="participant-title"),
            dcc.Dropdown(id='participant-dropdown3',
                         options=[{'label': participant, 'value': participant} for participant in participant_folders],
                         placeholder="Select Participant")
        ])
])

loading_card4 = dbc.Card([
    html.Div(
        [
            html.H6('Parameter Selection', className="participant-title"),
            dcc.Dropdown(id='parameter-selection3',
                         options=['Completion Time [s]','Success Rate'],
                         placeholder="Select Participant")
        ])
])

default_figure = go.Figure(data=[go.Scatter(x=[], y=[])],
                 layout=go.Layout(title="No data available for the selected filters."))
default_figure.update_layout(
    xaxis=dict(showgrid=False, showline=False,  # Hide x-axis line
               zeroline=False,  # Hide zero line
               showticklabels=False,  # Hide tick labels
               showspikes=False),
    yaxis=dict(showgrid=False, showline=False,  # Hide x-axis line
               zeroline=False,  # Hide zero line
               showticklabels=False),
    plot_bgcolor='black',  # Set background color to black
    paper_bgcolor='black',  # Set plot's paper background color to black
    font=dict(color='white')  # Set font color to white for better visibility
)
learning_effect_per_participant = dbc.Card([
    html.Div(
        [
            html.H5('Facet Plot of Learning Effect', className="card-title"),
            html.Br(),
            dcc.Graph(id='graph-container3',  figure=default_figure)  # Assign the default figure here
        ]
    )
],
    body=True
)


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.H3("Learning Effect Analysis"), className="d-grid justify-content-md-center"),
            ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(loading_card3, width=4),
            dbc.Col(loading_card4, width=4)

        ], ),
        dbc.Row([
            dbc.Col(learning_effect_per_participant, width=12),
        ], align="stretch", ),
    ],
    # fluid=True,
)


# Callback to update graph based on selected participant
@app.callback(
    Output('graph-container3', 'figure'),
    [Input('participant-dropdown3', 'value'),
     Input('parameter-selection3', 'value')]
)
def update_graph(participant, parameter_string):
    # Load the CSV file starting with 'Mazes-Summary'
    summary_file = [file for file in os.listdir(os.path.join(folder_path, participant)) if file.startswith('Mazes-Summary')][0]
    csv_path = os.path.join(folder_path, participant, summary_file)
    data = pd.read_csv(csv_path)

    # Plot facets
    fig = plot_facets(data, parameter_string)
    fig.update_layout(plot_bgcolor='black',  # Set background color to black
        paper_bgcolor='black',  # Set plot's paper background color to black
        font=dict(color='white'),  # Set font color to white for better visibility
        xaxis = dict(
        gridcolor='#474747',  # Set x-axis grid color to red
        gridwidth=3),  # Set x-axis grid width to 2),
        yaxis = dict(
        gridcolor='#474747',  # Set y-axis grid color to blue
        gridwidth=3),  # Set x-axis grid width to 2
    )
    return fig

