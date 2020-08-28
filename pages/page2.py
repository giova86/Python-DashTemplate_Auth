import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input,State
from dash import no_update
import random
from flask_login import current_user
import time
from functools import wraps
import pandas as pd
import plotly.express as px

from server import app

login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)

location = dcc.Location(id='page2-url',refresh=True)

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

fig = px.scatter(df, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=60
                 )



def layout():
    #if current_user.is_authenticated:
    return dbc.Row(
        dbc.Col(
            [
                location,
                html.Div(id='page1-login-trigger'),

                html.H1('Page2'),
                html.Br(),

                html.H5('Welcome to Page2!'),
                html.Br(),

                dcc.Graph(
                    id='life-exp-vs-gdp',
                    figure=fig
                ),
                html.Br(),
                dcc.Graph(id='graph-with-slider'),
                dcc.Slider(
                    id='year-slider',
                    min=df2['year'].min(),
                    max=df2['year'].max(),
                    value=df2['year'].min(),
                    marks={str(year): str(year) for year in df2['year'].unique()},
                    step=None
                ),
                html.Br(),

            ],
            width=12
        )

    )

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df2[df2.year == selected_year]

    fig = px.scatter(filtered_df,
                     x="gdpPercap",
                     y="lifeExp",
                     size="pop",
                     color="continent",
                     hover_name="country",
                     log_x=True,
                     size_max=55)

    fig.update_layout(transition_duration=500)

    return fig
# @app.callback(
#     Output('page1-test','src'),
#     [Input('page1-test-trigger','children')]
# )
# def page1_test_update(trigger):
#     '''
#     updates iframe with example.com
#     '''
#     time.sleep(2)
#     return 'http://example.com/'
