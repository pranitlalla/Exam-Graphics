import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(style={'backgroundColor': '#1D2B53'}, children=[
    html.Div([
        html.Div([
            html.Div([
                html.H1('Sardar Patel Institute of Technology', style={'textAlign': 'center', 'color': 'white', 'padding': '20px'}),
                html.Hr(style={'borderColor': 'white'}),
                html.Div([
                    html.Div(
                        dcc.Link(f"{page['name']}", href=page["relative_path"], style={'backgroundColor': '#1D2B53', 'color': 'white', 'border': 'none'}, className='btn btn-primary btn-block mb-3')
                    ) for page in dash.page_registry.values()
                ]),
                html.Hr(style={'borderColor': 'white'}),
            ], style={'width': '100%'}),
        ], style={'display': 'flex', 'justifyContent': 'center'}),
        html.Div(children=[dash.page_container])
    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})
])

if __name__ == '__main__':
    app.run(debug=True)
