#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('../tradingBot/OUT/data.csv', sep = '\t')
balance = pd.read_csv('../tradingBot/OUT/balance.txt', sep = '\t')


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                go.Candlestick(x=df.date,
                    open=df.open,
                    high=df.high,
                    low=df.low,
                    close=df.close),
                go.Scatter(
                    x=df.date,
                    y=balance.Balance,
                    name='yaxis2 data',
                    yaxis='y2')
            ],
            'layout': go.Layout(
                legend=dict(x=0, y=1),
                title =  'Mes Couilles',
                xaxis = {},
                yaxis = {'title' : 'Price (USD)', 'matches' : 'x'},
                yaxis2 = {'title' : 'Profit (%)', 'overlaying' : 'y', 'side' : 'right'},
            )
        }
    ),
    dcc.Graph(id='chart')
])

@app.callback(
    Output('chart', 'figure'),
    [Input('x-range-slider', 'value')])
def update_graph(xZoom):

    ddf = df[df.date == xZoom]
    dbalance = balance[df.date == xZoom]
    
    return {
        'data': [go.Candlestick(x=ddf.date,
                    open=ddf.open,
                    high=ddf.high,
                    low=ddf.low,
                    close=ddf.close),
                go.Scatter(
                    x=ddf.date,
                    y=dbalance.Balance,
                    name='yaxis2 data',
                    yaxis='y2')


        ],
        'layout': go.Layout(
                legend=dict(x=0, y=1),
                title =  'Mes Couilles',
                xaxis = {},
                yaxis = {'title' : 'Price (USD)', 'range': [ddf.low.min()*0.95,ddf.high.max()*1.05]},
                yaxis2 = {'title' : 'Profit (%)', 'overlaying' : 'y', 'side' : 'right', 'range': [dbalance.Balance.min()*0.95,dbalance.Balance.max()*1.05]}
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
