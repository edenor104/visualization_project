import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import numpy as np
from scipy.stats import gaussian_kde
import dash_bootstrap_components as dbc
from app import app
import os

# Load your DataFrame
combined_data_path = os.getcwd() + r"\Data\Excel Data\Experiment 1\raw_combined.csv"
df = pd.read_csv(combined_data_path)


loading_card1 = dbc.Card([
    html.Div(
        [
            html.H6('Maze selection', className="maze-title"),
            dcc.Dropdown(id='maze-type-dropdown',
                         options=['Maze1', 'Maze2', 'Maze3', 'Maze4'],
                         placeholder="Select Maze"),
        ])
])
loading_card2 = dbc.Card([
    html.Div(
        [
            html.H6('Condition selection', className="condition-title"),
            dcc.Dropdown(id='condition-dropdown',
                         options=['Multisensory (Audio and Visual)', 'Visual Only', 'Auditory Only', 'Invisible','Partial Visual Clash', 'Partial Audio Clash', 'Full Visual Clash', 'Full Audio clash'],
                         placeholder="Select Condition"),
        ])
])

# [{'label': i, 'value': i} for i in df['condition'].unique()]
loading_card3 = dbc.Card([
    html.Div(
        [
            html.H6('Participant selection', className="participant-title"),
            dcc.Dropdown(id='participant-dropdown',
                         options=[{'label': i, 'value': i} for i in df['Participant'].unique()],
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
    font=dict(color='white'))  # Set font color to white for better visibility

maze_path_graph = dbc.Card([
    html.Div(
        [
            html.H5('Heatmap Collisions Visualization', className="card-title"),
            html.Br(),
            dcc.Graph(id='maze-graph', figure=default_figure)
        ]
    )
],
    body=True
)

maze_collision_graph = dbc.Card([
    html.Div(
        [
            html.H5('Maze Path Maze', className="card-title"),
            html.Br(),
            dcc.Graph(id='maze-graph_collision', figure=default_figure)
        ]
    )
],
    body=True
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.H3("Spatial Visualization"), className="d-grid justify-content-md-center"),
            ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(loading_card1, width=4),
            dbc.Col(loading_card2, width=4),
            dbc.Col(loading_card3, width=4)

        ], ),
        dbc.Row([
            dbc.Col(maze_path_graph, width=6),
            dbc.Col(maze_collision_graph, width=6),
        ], align="stretch", ),
    ],
    # fluid=True,
)


# Callback to update graph based on dropdown values
@app.callback(
    Output('maze-graph', 'figure'),
    Output('maze-graph_collision', 'figure'),
    [Input('maze-type-dropdown', 'value'),
     Input('condition-dropdown', 'value'),
     Input('participant-dropdown', 'value')]
)
def update_graph(selected_maze_type, selected_condition_string, selected_participant):

    condition_conversion = {'Multisensory (Audio and Visual)': 'all', 'Visual Only': 'visual_only', 'Auditory Only':'audio_only', 'Invisible':'invisible', 'Partial Visual Clash':'contra_visual',
     'Partial Audio Clash':'contra_audio', 'Full Visual Clash':'const_contra_visual', 'Full Audio Clash':'const_contra_audio2'}

    selected_condition = condition_conversion[selected_condition_string]

    filtered_df = df[(df['maze_type'] == selected_maze_type) &
                     (df['condition'] == selected_condition) &
                     (df['Participant'] == selected_participant)].sort_values(by='time')
    filtered_df_collision = df[(df['maze_type'] == selected_maze_type) &
                               (df['condition'] == selected_condition) &
                               (df['collision_status'] != '0') & (df['Participant'] == selected_participant)]


    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        # Return a default figure or an indication that no data matches the filters
        fig3 = go.Figure(data=[go.Scatter(x=[], y=[])],
                  layout=go.Layout(title="No data available for the selected filters."))
        fig3.update_layout(
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

        fig4 = go.Figure(data=[go.Scatter(x=[], y=[])],
                  layout=go.Layout(title="No data available for the selected filters."))
        fig4.update_layout(
            xaxis=dict(showgrid=False, showline=False,  # Hide x-axis line
                       zeroline=False,  # Hide zero line
                       showticklabels=False,  # Hide tick labels
                       showspikes=False  # Hide spikes,
                       ),
            yaxis=dict(showgrid=False, showline=False,  # Hide x-axis line
                       zeroline=False,  # Hide zero line
                       showticklabels=False),
            plot_bgcolor='black',  # Set background color to black
            paper_bgcolor='black',  # Set plot's paper background color to black
            font=dict(color='white')  # Set font color to white for better visibility
        )

        return fig3, fig4

    maze_images = {
        'Maze1': 'assets/maze_1.png',
        'Maze2': 'assets/maze_2.png',
        'Maze3': 'assets/maze_3.png',
        'Maze4': 'assets/maze_4.png',
    }
    if selected_maze_type == 'Maze3':
        x_coor = -1.8
        y_coor = 3.9
        size_x = 4.5
        size_y = 5

    if selected_maze_type == 'Maze1':
        x_coor = -2.85
        y_coor = 3.65
        size_x = 4
        size_y = 5

    if selected_maze_type == 'Maze2':
        x_coor = -3.1
        y_coor = 3.85
        size_x = 5.7
        size_y = 5

    if selected_maze_type == 'Maze4':
        x_coor = -3.1
        y_coor = 3.95
        size_x = 4.2
        size_y = 5

    # Proceed with setting up the figure and animation if data is available
    fig = go.Figure()
    fig.add_layout_image(
        dict(
            source=maze_images.get(selected_maze_type),
            xref="x",
            yref="y",
            x=x_coor,
            y=y_coor,
            sizing="stretch",
            sizex=size_x,
            sizey=size_y,
            opacity=0.9,
            layer="below")
    )

    # Add frames for animation based on the filtered DataFrame
    frames = [
        go.Frame(data=[go.Scatter(x=[filtered_df.iloc[i]['z']], y=[-filtered_df.iloc[i]['x']], mode='markers+lines')])
        for i in range(len(filtered_df))]
    fig.frames = frames

    # Update the initial frame
    fig.add_trace(go.Scatter(x=filtered_df['z'], y=-filtered_df['x'], mode='markers+lines',
                             marker=dict(
                                 color='yellow',
                                 size=20, line=dict(
                                     color='White',
                                     width=6
                                 )), opacity=1))

    # Animation control
    fig.update_layout(updatemenus=[dict(type="buttons", showactive=False,
                                        y=1, x=0.5, xanchor='center', yanchor='top',
                                        buttons=[dict(label='Play',
                                                      method='animate',
                                                      args=[None, dict(frame=dict(duration=10, redraw=True),
                                                                       fromcurrent=True,
                                                                       transition=dict(duration=0))])])])
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    # Update layout to remove grid lines
    fig.update_layout(
        xaxis=dict(showgrid=False, showline=False,  # Hide x-axis line
        zeroline=False,  # Hide zero line
        showticklabels=False,  # Hide tick labels
        showspikes=False, range=[x_coor, x_coor + size_x]),  # Hide spikes
        yaxis=dict(showgrid=False, showline=False,  # Hide x-axis line
        zeroline=False,  # Hide zero line
        showticklabels=False,  # Hide tick labels
        showspikes=False, range=[y_coor - size_y, y_coor]),
        plot_bgcolor='black',  # Set background color to black
        paper_bgcolor='black',  # Set plot's paper background color to black
        font=dict(color='white')  # Set font color to white for better visibility
    )

    # Proceed with setting up the figure and animation if data is available
    fig2 = go.Figure()
    fig2.add_layout_image(
        dict(
            source=maze_images.get(selected_maze_type),
            xref="x",
            yref="y",
            x=x_coor,
            y=y_coor,
            sizing="stretch",
            sizex=size_x,
            sizey=size_y,
            opacity=0.9,
            layer="below")
    )

    # Calculate KDE
    x = filtered_df_collision['z']
    y = -filtered_df_collision['x']
    kde = gaussian_kde([x, y])
    X, Y = np.meshgrid(np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100))
    Z = kde([X.flatten(), Y.flatten()]).reshape(X.shape)

    # Add KDE as contour plot
    fig2.add_trace(go.Contour(x=np.linspace(x.min(), x.max(), 100),
                              y=np.linspace(y.min(), y.max(), 100),
                              z=Z, colorscale='Viridis', opacity=0.6))

    # Update layout to match image dimensions and remove axis labels
    fig2.update_layout(
        xaxis=dict(showgrid=False, showline=False,  # Hide x-axis line
        zeroline=False,  # Hide zero line
        showticklabels=False,  # Hide tick labels
        showspikes=False,  # Hide spikes,
        range=[x_coor, x_coor + size_x]),
        yaxis=dict(showgrid=False, showline=False,  # Hide x-axis line
        zeroline=False,  # Hide zero line
        showticklabels=False,  # Hide tick labels
        showspikes=False, range=[y_coor - size_y, y_coor]),
        plot_bgcolor='black',  # Set background color to black
        paper_bgcolor='black',  # Set plot's paper background color to black
        font=dict(color='white')  # Set font color to white for better visibility
    )

    return fig2, fig
