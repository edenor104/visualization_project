
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, callback, no_update, ctx
# Connect to main app.py file
from app import app
# from app import server

# Connect to your app pages
from apps import app1, app2, app3

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("When Vision Lies", className="display-4"),
        html.Hr(),
        html.P(
            "Visualization Project", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Spatial Visualization", href="/spatial_visualization", active="exact"),
                dbc.NavLink("Correlation Analysis", href="/correlation_analysis", active="exact"),
                dbc.NavLink("Learning Effect Analysis", href="/learning_effect", active="exact"),

            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[])

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/spatial_visualization":
        return app1.layout
    elif pathname == "/learning_effect":
        return app3.layout
    elif pathname == "/correlation_analysis":
        return app2.layout
    # If the user tries to reach a different page, return a 404 message
    return


if __name__ == '__main__':
    app.run(debug=False)
