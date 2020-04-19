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

def get_trajplot_data(states,path,column):
    
    data = pd.read_csv(path/'states_daily.csv',index_col=0)
    data = data[data['status'] == column].reset_index(drop=True)
    data['date'] = data['date'].apply(lambda x : datetime.datetime.strptime(x,'%Y-%m-%d').strftime('%d-%B'))
    for item in states:
        data[item] = pd.to_numeric(data[item],errors='coerce')
    data = data[['date'] + states]
    
    return data



def plot(path,states,column):
    
    if isinstance(states,list) == False:
        states = [states]
    data = get_trajplot_data(states,path,column)
    total = data.set_index('date').cumsum().reset_index(drop=False).loc[7:].reset_index(drop=True)
    data.iloc[:,1:] = data.iloc[:,1:].rolling(7).sum() #To be on the pessimistic side of analysis to account for data variabilit and reliability
    data = data.dropna().reset_index(drop=True)
    
    fig_dict = {
        "data" : [],
        "layout" : {},
        "frames" : []
    }
    fig_dict['layout']['xaxis'] = {'range' : [np.log(1),np.log(1000)], 'type' : 'log', 'title' : 'Total Cases'}
    fig_dict['layout']['yaxis'] = {'range' : [np.log(1),np.log(100)], 'type' : 'log', 'title' : 'Total new cases in past week'}
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["sliders"] = {
        "args": [
            "transition", {
                "duration": 100,
                "easing": "cubic-in-out"
            }
        ],
        "initialValue": data.loc[0,'date'],
        "plotlycommand": "animate",
        "values": data['date'].values.tolist(),
        "visible": True
    }
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 100, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 100,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Date:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 100, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }
    
    for state in states:
        x_data = [total.loc[0][state]]
        y_data = [data.loc[0][state]]
        data_dict = {
            'x' : x_data,
            'y' : y_data,
            'mode' : 'markers',
            'marker' : { 'size' : 10},
            'name' : state
        }
        fig_dict['data'].append(data_dict)
    
    for ind in data.index[1:]:
        frame = {'data' : [], 'name' : data.loc[ind,'date']}
        for state in states:
            x_data = total.loc[:ind][state].values.tolist()
            y_data = data.loc[:ind][state].values.tolist()
            data_dict = {
                'x' : x_data,
                'y' : y_data,
                'mode' : 'lines+markers',
                'marker' : { 'size' : 5},
                'name' : state
            }
            frame['data'].append(data_dict)
            
        fig_dict['frames'].append(frame)
        
        slider_step = {'args' : [
            [data.loc[ind,'date']],
            {'frame' : {'duration':100,'redraw' : True},
             'transition' : {'duration' : 0},
             'mode' : 'immediate'}
        ],
            'label':data.loc[ind,'date'],
            'method':'animate'}
        
        sliders_dict['steps'].append(slider_step)
        
    fig_dict['layout']['sliders'] = [sliders_dict]
    
    fig = go.Figure(fig_dict)
        
    fig.update_layout(
        font=dict( 
            family="Courier New, monospace"),
        height = 600,
        margin = dict(l=20,r=20,t=50,b=50)
        )
    
    return fig