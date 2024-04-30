import dash
from dash import html, dcc, callback, Input, Output
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

data=pd.read_csv("IT_COMPS.csv")

selected_columns = ['CLASS', 'PE V Elective', 'PE V Total marks(out of 100)including ISE+ESE', 'PE VI Elective', 'PE VI Total marks(out of 100)including ISE+ESE']
df = data[selected_columns]

dash.register_page(__name__)

layout = html.Div(style={'background-color':'#1D2B53'},children=[
    html.H1(children='Average Marks by Elective Subject', style={'textAlign':'center','background-color':'1D2B53','color':'white','padding':'20px'}),
    html.Div(style={'margin': '0 auto', 'width': '1200px', 'display': 'flex', 'justify-content': 'space-between'}, children=[
        html.Div([
            html.Label('Elective Type:'),
            dcc.Dropdown(
                id='elective-dropdown',
                options=[
                    {'label': 'PE V Elective', 'value': 'PE V'},
                    {'label': 'PE VI Elective', 'value': 'PE VI'}
                ],
                value='PE V',
                style={'width': '100%','color':'black','margin-top': '10px'}
            ),
        ], style={'width': '32%','margin-bottom':'30px','color':'white'}),
        html.Div([
            html.Label("Select Number of Top Courses:"),
            dcc.Input(
                id='top-courses-input',
                type='number',
                value=3,
                min=1,
                max=len(df['PE V Elective'].unique()),
                style={'width': '100%', 'margin-top': '10px','height':'37px'}
            )
        ], style={'width': '32%','margin-bottom':'30px','color':'white'}),
        html.Div([
            html.Label("Select Class:", style={'color': 'white'}),
            dcc.Dropdown(
                id='class-dropdown',
                options=[
                    {'label': 'COMPS', 'value': 'COMPS'},
                    {'label': 'IT', 'value': 'IT'},
                    {'label': 'ETRX', 'value': 'ETRX'}
                ],
                value=['COMPS', 'IT', 'ETRX'],
                multi=True,
                style={'width': '100%', 'margin-top': '10px'}
            )
        ], style={'width': '32%','margin-bottom':'30px','color':'black'}),
    ]),
    html.Div(style={'margin': '0 auto', 'width': '1200px'}, children=[
        dcc.Graph(id='top-courses-chart', style={'width': '100%', 'height': '800px'}),
    ]),
    html.Div(style={'margin': '0 auto', 'width': '1200px'}, children=[
        dcc.Graph(id='bar-chart', style={'width': '100%', 'height': '800px'})
    ])
])

@callback(
    Output('top-courses-chart', 'figure'),
    Output('bar-chart', 'figure'),
    [Input('elective-dropdown', 'value'),
     Input('top-courses-input', 'value'),
     Input('class-dropdown', 'value')]
)
def update_charts(selected_elective, top_courses, selected_class):
    
    filtered_df = df[df['CLASS'].isin(selected_class)]

    elective_column = f'{selected_elective} Elective'
    marks_column = f'{selected_elective} Total marks(out of 100)including ISE+ESE'

    top_courses_counts = filtered_df[elective_column].value_counts().head(top_courses)

    top_courses_fig = px.bar(
        top_courses_counts,
        x=top_courses_counts.values,
        y=top_courses_counts.index,

orientation='h',
        labels={'x': 'Frequency', 'y': 'Course'},
        title=f'Top {top_courses} {selected_elective} Elective Courses',
        color=top_courses_counts.index,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    top_courses_fig.update_layout(plot_bgcolor='#ffffff')

    avg_marks_by_subject = filtered_df.groupby(elective_column)[marks_column].mean().reset_index()
    avg_marks_by_subject = avg_marks_by_subject.sort_values(by=marks_column, ascending=False)

    avg_marks_fig = px.bar(
        avg_marks_by_subject,
        x=marks_column,
        y=elective_column,
        labels={marks_column: 'Average Marks', elective_column: 'Elective Subject'},
        title=f'Average Marks by {selected_elective} Elective',
        orientation='h',
        height=500,
        color=elective_column,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    avg_marks_fig.update_layout(plot_bgcolor='#ffffff')

    return top_courses_fig, avg_marks_fig