import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output


#create a dataframe
df = pd.DataFrame(
    {'wdg': [10,10,10,20,20,20,30,30,30,40],
     'id': np.arange(0,100,10),
     'b': np.random.rand(10)*100,
     'c': np.random.rand(10)*100,
     'd': np.random.rand(10)*100,
     'e': np.random.rand(10)*100,
     'f': np.random.rand(10)*100,
     'g': np.random.rand(10)*100,
     'h': np.random.rand(10)*100,
     'k': np.random.rand(10)*100},
     
    columns=['wdg','id','b','c','d','e','f','g','h','k'])



app = dash.Dash()

colors = {
    'background': '#111111',
    'text': '#000000'
}

#function to generate perfromance table from pandas dataframe
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app.layout = html.Div([
    html.H1(
        children='Perfomance database web app',
        style={
            'textAlign': 'center',
            'color': colors['text']}
    ),

    html.Div([
        dcc.Dropdown(
            id='dropdown1',
            options=[{'label': i, 'value': i} for i in df.wdg.unique()],
            value='10'
        ),
        dcc.Dropdown(
            id='dropdown2',
            #options=[{'label': i, 'value': i} for i in mtrid_indicators],
            #value='1'
        ),
    ],
    style={'width': '49%', 'display': 'inline-block'}
    ),

    html.Div(id='tablecontainer'),
    
    html.Div(
        dcc.Graph(
            id='graph',

            style={'width':'600','height':'500'}
        ),
        style={'display':'inline-block'}
    ),

    ],
style={'width': '100%', 'display': 'inline-block'}
)

#callback to update dropdown
@app.callback(
    Output(component_id='dropdown2',component_property='options'),
    [Input(component_id='dropdown1',component_property='value')]
)


def update_dropdown2(wdg):
    wdgarray=df[ df['wdg'] == wdg ]['id'],
    return [{'label':i,'value':i} for i in wdgarray]

#callback to update graph
@app.callback(
    Output('graph', 'figure'), 
    [Input('dropdown1', 'value')]
)

def update_graph(row):
    dff = df.iloc[int(row/10)].values # update with your own logic
    return {
        'data': [
                    go.Scatter(
                        x=np.arange(0,80,10),
                        y=dff,
                        mode='lines+markers',
                        line = dict(width = 5,color = 'rgb(200, 0, 0)'),
                        name='Torque curve',
                        marker = dict(
                        size = 10,
                        color = 'rgba(200, 0, 0, .9)',
                        line = dict(width = 2,color='rgb(0, 0, 0)')
                        )
                    ),
                ],
        'layout': go.Layout(
                    title='Torque Speed curve',

                    xaxis=dict(
        #               type='line',
                        title='Speed - (RPM)',
                        showgrid=True,
                        #zeroline=True,
                        showline=True,
                        gridcolor='#bdbdbd',
                        mirror="ticks",
                        ticks="inside",
                        tickwidth=1,
                        linewidth=2,
                        range=[0,100]
                    ),
                    yaxis=dict(
                        title= 'Torque - (lb-ft)',
                        titlefont=dict( color='rgb(200, 0, 0)' ),
                        tickfont=dict( color='rgb(200, 0, 0)' ),
                        range=[0, 120],
                        showgrid=True,
                        #zeroline=True,
                        showline=True,
                        gridcolor='#bdbdbd',
                        mirror="ticks",
                        ticks="inside",
                        tickwidth=1,
                        linewidth=2
                    ),
                    margin={'l': 60, 'b': 40, 't': 30, 'r': 60},
                    #legend={'x': 0.5, 'y': 1},
                    hovermode='closest',
                    showlegend=False,
                )
        }

if __name__ == '__main__':
    app.run_server()