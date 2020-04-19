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

def get_tsplot_data(path,state):
    data = pd.read_csv(path/'states_daily.csv',index_col=0)
    data = pd.pivot_table(data,columns='status',values=state,index='date')
    data = data.cumsum()
    data = data.reset_index(drop=False)
    
    return data

def plot(path,state):

    data = get_tsplot_data(path,state)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x = data['date'], y = data['Confirmed'], mode = 'lines', name = 'Confirmed'))
    fig.add_trace(go.Scatter(x = data['date'], y = data['Deceased'], mode = 'markers', name = 'Deceased'))
    fig.add_trace(go.Scatter(x = data['date'], y = data['Recovered'], mode = 'lines+markers', name = 'Recovered'))
    
    fig.update_layout(
        title = state,
        title_font = {'size' : 22,
                      'family' : 'Courier New, monospace'
                     },
        margin = dict(l=20,r=20,t=50,b=50)
            
    )
    return fig

if __name__ == "__main__":
    pass