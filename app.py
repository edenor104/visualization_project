from dash import Dash
import dash_bootstrap_components as dbc

# meta_tags are required for the app layout to be mobile responsive
# app = dash.Dash(__name__, suppress_callback_exceptions=True,
#                 meta_tags=[{'name': 'AutoTriage',
#                             'content': 'width=device-width, initial-scale=1.0'}]
#                 )

app = Dash(external_stylesheets=[dbc.themes.CYBORG])
# server = app.server