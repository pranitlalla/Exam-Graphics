import dash
from dash import html, dcc, callback, Input, Output
from dash import dash_table
import plotly.express as px
import pandas as pd

df = pd.read_excel('all.xlsx')

dash.register_page(__name__)

layout = html.Div(style={'background-color':'#1D2B53'},children=[
    html.H1(children='Semester Results', style={'textAlign':'center','background-color':'1D2B53','color':'white','padding':'20px'}),
    html.Div(style={'margin': '0 auto', 'width': '1000px', 'display': 'flex', 'justify-content': 'space-between'}, children=[
        html.Div([
            html.Label('Class:', style={'color': 'white'}),
            dcc.Dropdown(
                id='class-dropdown',
                options=[{'label': i, 'value': i} for i in df['Class'].unique()],
                value=df['Class'].unique(),
                multi=True
            ),
        ], style={'width': '50%','margin-bottom':'30px','color':'black'}),
        html.Div([
            html.Label('Semester:', style={'color': 'white'}),
            dcc.Dropdown(
                id='semester-dropdown',
                options=[{'label': i, 'value': i} for i in df['Semester'].unique()],
                value=df['Semester'].unique()[0],
                clearable=False
            ),
        ], style={'width': '50%','margin-bottom':'30px','color':'black'}),
    ]),
    html.Div(style={'margin': '0 auto', 'width': '1000px', 'display': 'flex', 'justify-content': 'space-between'}, children=[
        html.Div([
            html.Label('Subjects:', style={'color': 'white'}),
            dcc.Dropdown(
                id='subject-dropdown',
                options=[{'label': i, 'value': i} for i in df.select_dtypes(include=['number']).columns if i != 'UID' and i != 'Semester' and i!='CGPA'],
                value=df.select_dtypes(include=['number']).columns,
                multi=True
            ),
        ], style={'width': '70%','margin-bottom':'30px','color':'black'}),
        html.Div([
            html.Label('Status:', style={'color': 'white'}),
            dcc.Dropdown(
                id='status-dropdown',
                options=[{'label': i, 'value': i} for i in df['Status'].unique()],
                value=df['Status'].unique(),
                multi=True
            ),
        ], style={'width': '30%','margin-bottom':'30px','color':'black'}),
    ]),
    html.Div(style={'margin': '0 auto', 'width': '1000px'}, children=[
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'height': '600px', 'width': '1000px', 'overflowY': 'scroll', 'overflowX': 'scroll'},
            style_cell={'whiteSpace': 'normal', 'height': 'auto', 'textAlign': 'left'},
        )
    ]),
    html.Div(style={'margin': '0 auto', 'width': '1000px'}, children=[
        dcc.Graph(id='most-scoring-subject')
    ]),
    html.Div(style={'margin': '0 auto', 'width': '1000px'}, children=[
        dcc.Graph(id='unsuccessful-scores')
    ]),
    html.Div(style={'margin': '0 auto', 'width': '1000px'}, children=[
        dcc.Graph(id='status-pie-chart')
    ]),
    html.Div(style={'margin': '0 auto', 'width': '1000px'}, children=[
        dcc.Graph(id='box-plot')
    ]),
    html.Div(style={'margin': '0 auto', 'width': '1000px'}, children=[
        dcc.Graph(id='heatmap')
    ])
])

@callback(
    Output('table', 'columns'),
    Output('table', 'data'),
    [Input('class-dropdown', 'value'),
     Input('semester-dropdown', 'value'),
     Input('subject-dropdown', 'value'),
     Input('status-dropdown', 'value')],
     allow_duplicate=True
)
def update_table(class_values, semester_value, subject_values, status_values):
    selected_columns = ['Class', 'Semester', 'UID', 'Name', 'Status'] + subject_values + ['CGPA']
    filtered_df = df[(df['Class'].isin(class_values)) & (df['Semester'] == semester_value) & (df['Status'].isin(status_values))]
    filtered_df = filtered_df[selected_columns]
    columns = [{"name": i, "id": i} for i in filtered_df.columns]
    data = filtered_df.to_dict('records')

    return columns, data

@callback(
    Output('most-scoring-subject', 'figure'),
    [Input('table', 'data'),
     Input('subject-dropdown', 'value')],
     allow_duplicate=True
)
def update_most_scoring_subject(rows, subject_values):
    df = pd.DataFrame.from_dict(rows)
    total_cols = [col for col in df if 'Total' in col and col in subject_values]
    avg_scores = df[total_cols].mean()
    fig = px.bar(avg_scores.sort_values(ascending=False))
    fig.update_layout(title='Most Scoring Subjects', margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor='white', width=1000, height=600)
    return fig

@callback(
    Output('unsuccessful-scores', 'figure'),
    [Input('table', 'data')],
    allow_duplicate=True
)
def update_unsuccessful_scores(rows):
    df = pd.DataFrame.from_dict(rows)
    subjects = []
    unsucess_df = df[df['Status']=='Unsuccessful']
    for col in unsucess_df.columns:
        if 'Total' in col:
            subjects.append(col)
    df = unsucess_df[subjects]
    new_df = pd.DataFrame({
        'subject': df.columns,
        'count_of_zeros': (df == 0).sum()
    })
    new_df = new_df.reset_index(drop=True)
    new_df=new_df.sort_values(by=['count_of_zeros'],ascending=True)
    fig = px.bar(new_df, x='subject', y='count_of_zeros')
    fig.update_layout(title='Distribution of Failed Students', margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor='white', width=1000, height=600)
    return fig

@callback(
    Output('status-pie-chart', 'figure'),
    [Input('table', 'data')],
    allow_duplicate=True
)
def update_status_pie_chart(rows):
    df = pd.DataFrame.from_dict(rows)
    status_counts = df['Status'].value_counts()
    fig = px.pie(values=status_counts, names=status_counts.index, title='Status Counts')
    fig.update_layout(title='Status of Pass', margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor='white', width=1000, height=600)
    return fig

@callback(
    Output('box-plot', 'figure'),
    [Input('table', 'data'),
     Input('subject-dropdown', 'value')],
     allow_duplicate=True
)
def update_box_plot(rows, subject_values):
    df = pd.DataFrame.from_dict(rows)
    fig = px.box(df, y=[col for col in df if 'Total' in col and col in subject_values])
    fig.update_layout(title='Distribution of Scores by Subject', margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor='white', width=1000, height=600)
    return fig

@callback(
    Output('heatmap', 'figure'),
    [Input('table', 'data'),
     Input('subject-dropdown', 'value')],
     allow_duplicate=True
)
def update_heatmap(rows, subject_values):
    df = pd.DataFrame.from_dict(rows)
    corr = df[[col for col in df if 'Total' in col and col in subject_values]].corr()
    fig = px.imshow(corr, text_auto=True)
    fig.update_layout(title='Correlation between Scores in Different Subjects', margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor='white', width=1000, height=600)
    return fig
