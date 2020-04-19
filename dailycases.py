import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import warnings
import datetime 
from pathlib import Path
warnings.filterwarnings('ignore')

def get_barplot_data(state,path):
    
    data = pd.read_csv(path/'states_daily.csv',index_col=0)
    data['date'] = data['date'].apply(lambda x : datetime.datetime.strptime(x,'%Y-%m-%d').strftime('%d-%B'))
    data[state] = pd.to_numeric(data[state],errors='coerce')
    
    return data

def plot(path,state):
    
    data = get_barplot_data(state,path)
    
    conf = data[data['status'] == 'Confirmed'][state].values.tolist()
    dead = data[data['status'] == 'Deceased'][state].values.tolist()
    recv = data[data['status'] == 'Recovered'][state].values.tolist()
    date = data['date'].unique()
    
    fig = go.Figure()

    fig.add_trace(go.Bar(x=date,y=conf,base=[0]*len(conf),marker_color='#400082',name='Confirmed'))
    fig.add_trace(go.Bar(x=date,y=dead,base=[-1*item for item in dead],marker_color='#dd2c00',name='Deceased'))
    fig.add_trace(go.Bar(x=date,y=recv,base=[0]*len(recv),marker_color='#2b580c',name='Recovered'))
                  
    fig.update_layout(
        title="Daily Cases - "+ state,
        font=dict(
            family="Courier New, monospace"),
        margin = dict(l=20,r=20,t=50,b=50)
        )
    
    return fig

def sirplot(path,state):
    data = get_barplot_data(state,path)

    conf = data[data['status'] == 'Confirmed'][state].rolling(5).mean().dropna()
    dead = data[data['status'] == 'Deceased'][state].rolling(5).mean().dropna()
    recv = data[data['status'] == 'Recovered'][state].rolling(5).mean().dropna()
    date = data.loc[12:,'date'].unique()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date,y=conf,marker_color='#400082',name='Confirmed'))
    fig.add_trace(go.Scatter(x=date,y=dead,marker_color='#dd2c00',name='Deceased'))
    fig.add_trace(go.Scatter(x=date,y=recv,marker_color='#2b580c',name='Recovered'))

    fig.show()