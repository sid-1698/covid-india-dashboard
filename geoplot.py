import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import warnings
import datetime 
from pathlib import Path
import json
warnings.filterwarnings('ignore')

def get_statewise_data(path):
    
    data = pd.read_csv(path/'states_daily.csv',index_col=0)
    data.drop('India',axis=1,inplace=True)
    data = pd.pivot_table(data,columns='status',values=[item for item in data.columns if ((item != 'status')&(item != 'date'))],index='date')
    data = data.sum().unstack(1).reset_index(drop=False)
    data.columns = ['State','Positive','Deceased','Recovered']
    
    return data

def plot1(path):
    
    data = get_statewise_data(path)
    jsonpath = path/'GeoJson/'
    with open(jsonpath/'india.json') as file:
        geojson = json.load(file)
        
    fig = px.choropleth(data, geojson=geojson, color="Positive",hover_data=['State'],
                           locations="State", featureidkey="properties.st_nm", projection="mercator",
                    color_continuous_scale="reds")

    fig.update_geos(fitbounds="locations", visible=False)

    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        clickmode = 'event+select',
        font=dict(
            family="Courier New, monospace")
        )
    
    return fig

def plot2(path,state):
    
    filename = state + '.csv'
    data = pd.read_csv(path/'States_Data'/filename,index_col=0)
    jsonfile = state.replace(' ','').lower()+'.json'
    jsonpath = path/'GeoJson/'
    jsonfile = jsonpath/jsonfile

    with open(jsonfile) as file:
        geojson = json.load(file)
    districts = [item['properties']['district'] for item in geojson['features']]  
    for item in districts:
        if item not in data.District.values:
            data.loc[len(data)] = pd.Series([item,0,0],index=['District','Total_Cases','Cases_Today'])
    fig = px.choropleth(data, geojson=geojson, color="Total_Cases",
                           locations="District", featureidkey="properties.district", projection="mercator",
                    color_continuous_scale="reds")

    fig.update_geos(fitbounds="locations", visible=False)

    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        title={'text' : state},
        hovermode = 'closest',
        font=dict(
            family="Courier New, monospace")
        )
    return fig