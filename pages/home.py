import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div(style={'background-color':'1D2B53','height': '100vh'}, children=[
    html.H1(''),
    html.Div(''),
])