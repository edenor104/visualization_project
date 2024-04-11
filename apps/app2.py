import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import numpy as np
import dash_bootstrap_components as dbc
from app import app
import os

correlation_data_path = os.getcwd() + r"\Data\Excel Data\Questionnaire Analysis\correlation_analysis.xlsx"

# Load your DataFrame
df = pd.read_excel(correlation_data_path)


loading_card3 = dbc.Card([
    html.Div(
        [
            html.Label('X-axis:'),
            dcc.Dropdown(id='x-dropdown',
                         options=['Normalized Mean Time', 'Normalized Mean Success'])
        ])
])

loading_card4 = dbc.Card([
    html.Div(
        [
            html.Label('Y-axis:'),
            dcc.Dropdown(id='y-dropdown',
                         options=['Normalized Gaming Score', 'Normalized Navigation Score'])
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
    font=dict(color='white'))  # Set font color to white for better visibility


learning_effect_per_participant = dbc.Card([
    html.Div(
        [
            html.H5('Correlation Analysis', className="card-title"),
            html.Br(),
            dcc.Graph(id='corr-graph',  figure=default_figure)
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
            dbc.Col(loading_card3, width=6),
            dbc.Col(loading_card4, width=6)

        ], ),
        dbc.Row([
            dbc.Col(learning_effect_per_participant, width=12),
        ], align="stretch", ),
    ],
    # fluid=True,
)

# Callback to update graph based on dropdown values
@app.callback(
    Output('corr-graph', 'figure'),
    [Input('x-dropdown', 'value'),
     Input('y-dropdown', 'value')]
)
def update_graph(selected_x, selected_y):
    converstion_selection = {'Normalized Gaming Score': 'normalized gaming score', 'Normalized Navigation Score':'normalize navigation score Score','Normalized Mean Time':'normalized mean time', 'Normalized Mean Success':'normalized mean success'}
    selection_conv_x = converstion_selection[selected_x]
    selection_conv_y = converstion_selection[selected_y]

    # Scatter plot
    fig = go.Figure()
    for sex in df['sex'].unique():
        data_subset = df[df['sex'] == sex]
        fig.add_trace(go.Scatter(x=data_subset[selection_conv_x], y=data_subset[selection_conv_y], mode='markers',
                                 name=sex, marker=dict(color='#5E84AD' if sex == 'm' else '#C06AB7', size=20)))

    # Calculate Pearson's r
    pearson_r = np.corrcoef(df[selection_conv_x], df[selection_conv_y])[0, 1]

    # Calculate linear regression parameters
    slope, intercept = np.polyfit(df[selection_conv_x], df[selection_conv_y], 1)
    linear_equation = f'y = {slope:.2f}x + {intercept:.2f}'

    # Overlay regression line
    x_range = np.linspace(df[selection_conv_x].min(), df[selection_conv_x].max(), 100)
    y_range = slope * x_range + intercept
    fig.add_trace(go.Scatter(x=x_range, y=y_range, mode='lines', name='Regression Line', marker=dict(color='#D5D5D5')))

    # Set axis labels
    fig.update_layout(xaxis_title=selected_x, yaxis_title=selected_y)
    fig.update_traces(line=dict(width=4))

    # Set title as Pearson's r and linear equation
    fig.update_layout(title=f"Pearson's r = {pearson_r:.2f}<br>{linear_equation}")
    fig.update_layout(plot_bgcolor='black',  # Set background color to black
        paper_bgcolor='black',  # Set plot's paper background color to black
        font=dict(color='#E2E2E2'),  # Set font color to white for better visibility
        xaxis=dict(
              gridcolor='#474747',  # Set x-axis grid color to red
              gridwidth=3,  # Set x-axis grid width to 2

        ),
        yaxis=dict(
              gridcolor='#474747',  # Set y-axis grid color to blue
              gridwidth=3  # Set x-axis grid width to 2

        ),
    )
    return fig

