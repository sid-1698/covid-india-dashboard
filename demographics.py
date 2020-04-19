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


def plot1(path):   
    
    data = pd.read_csv(path/'raw_data.csv',index_col = 0)
    fig = make_subplots(rows=1,cols=2,specs=[[{'type':'domain'}, {'type':'domain'}]])
    
    values = data['Gender'].value_counts(dropna=False).values.tolist()
    labels = data['Gender'].value_counts(dropna=False).index.tolist()
    labels = ['Missing','Male','Female']
    
    fig.add_trace(go.Pie(labels=labels,values=values,textinfo='label+percent',insidetextorientation='radial'),1,1)
    fig.update_traces(hole = 0.35)
    fig.update_layout(annotations = [dict(text='Gender',x=0.15,y=0.5,font_size=18,showarrow=False)])
    
    data['Transmission_Type'] = data['Transmission_Type'].apply(lambda x : 'Unknown' if str(x) == 'nan' else str(x).strip())
    values = data['Transmission_Type'].value_counts().values.tolist()
    labels = data['Transmission_Type'].value_counts().index.tolist()
    
    for label,value in zip(labels,values):
        if ((label == 'TBD') | (label == 'Unknown')):
            values.append(value)
    labels.append('Unknown')
    labels[labels.index('Unknown')] = 'Missing'
    values[-2] = values[-2] + values[-1]
    values = values[:-1]
    values.insert(0,sum(values[:-1]))
    labels.insert(0,'Transmission')
    parents = ['','Unknown','Transmission','Unknown','Transmission','Transmission']
    
    fig.add_trace(go.Sunburst(labels=labels,parents=parents,values=values,branchvalues='total',textinfo='label+percent root',insidetextorientation='radial'),1,2)
       
    fig.update_traces(hoverinfo='value',textfont_size=15)
    
    fig.update_layout(
        font=dict(
            family="Courier New, monospace"),
        showlegend=False,
        margin = dict(l=20,r=20,t=50,b=50)
        )
    
    return fig

def plot2(path):
    
    data = pd.read_csv(path/'raw_data.csv',index_col=0)
    
    fig= go.Figure()

    y1 = data[data['Curr_Status'] == 'Hospitalized']['Age'].values.tolist()
    fig.add_trace(go.Box(y=y1,name='Hospitalized',boxpoints='all',whiskerwidth=0.2,fillcolor='#084177'))

    y3 = data[data['Curr_Status'] == 'Deceased']['Age'].values.tolist()
    fig.add_trace(go.Box(y=y3,name='Deceased',boxpoints='all',whiskerwidth=0.2,fillcolor='#ff1e56'))

    y2 = data[data['Curr_Status'] == 'Recovered']['Age'].values.tolist()
    fig.add_trace(go.Box(y=y2,name='Recovered',boxpoints='all',whiskerwidth=0.2,fillcolor='#00bdaa'))



    fig.update_layout(
        font=dict(
            family="Courier New, monospace"),
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=5,
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        margin=dict(l=20,r=20,t=50,b=50),
        showlegend=False
    )
    
    return fig