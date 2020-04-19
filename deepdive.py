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

def get_quadrantplot_data(path):
    
    labs = pd.read_csv(path/'ICMRTestingLabs.csv')
    population = pd.read_csv(path/'population_india_census2011.csv',index_col=0)
    test = pd.read_csv(path/'StatewiseTestingDetails.csv',index_col=0)
    hospitals = pd.read_csv(path/'HospitalBedsIndia.csv',index_col=0)
    states = pd.read_csv(path/'states_daily.csv',index_col=0)
    
    states.drop('India',axis=1,inplace=True)
    states = pd.pivot_table(states,columns='status',values=[item for item in states.columns if ((item != 'status')&(item != 'date'))],index='date')
    states = states.sum().unstack(1).reset_index(drop=False)
    states.columns = ['State','Positive','Deceased','Recovered']

    labs = labs['state'].value_counts().reset_index(drop=False)
    labs.columns = ['State','Labs']
    
    test = test.groupby('State')['Samples'].max().reset_index(drop=False)
    
    hospitals = hospitals[['State','Total_Hospitals','Total_Beds']]
    hospitals = hospitals.iloc[:-1,:]
    
    data = population.merge(labs,left_on='State',right_on='State',how='outer')
    data = data.merge(test,left_on='State',right_on='State',how='outer')
    data = data.merge(hospitals,left_on='State',right_on='State',how='outer')
    data = data.merge(states,left_on='State',right_on='State',how='outer')
    
    data['Area/Lab'] = (data['Area']/data['Labs'])/1000
    data['People/Lab'] = (data['Population']/data['Labs'])/1000000
    data['Area/Hospital'] = (data['Area']/data['Total_Hospitals'])/10
    data['People/Hospital'] = (data['Population']/data['Total_Hospitals'])/1000 
    
    return data


def plot1(path):

    data = get_quadrantplot_data(path)

    fig = make_subplots(rows=1,cols=2)
    
    states = data['State'].values.tolist()
    deceased = data['Deceased'].values.tolist()
    
    fig.add_trace(go.Scatter(x=data['People/Hospital'],y=data['Area/Hospital'],text=['State : {} <br> Deceased : {}'.format(state,dec) for state,dec in zip(states,deceased)],
                             hoverinfo = 'text',mode='markers',marker=dict(size=15,color=data['Deceased'],colorscale='inferno',showscale=True)),1,2)
    fig.add_shape(
        type='rect',
        x0=0,y0=0,x1=150,y1=225,xref='x2',
        fillcolor='#64e291',
        opacity=0.3
    )
    
    fig.add_shape(
        type='rect',
        x0=150,y0=0,x1=300,y1=225,xref='x2',
        fillcolor='#e6e56c',
        opacity=0.3
    )
    
    fig.add_shape(
        type='rect',
        x0=0,y0=225,x1=150,y1=450,xref='x2',
        fillcolor='#e6e56c',
        opacity=0.3
    )
    
    fig.add_shape(
        type='rect',
        x0=150,y0=225,x1=300,y1=450,xref='x2',
        fillcolor='#eb7070',
        opacity=0.3
    )
    
    hospitals = data['Total_Hospitals'].values.tolist()
    fig.add_trace(go.Scatter(x=data['Total_Beds']/100,y=data['Recovered'],text=['State : {} <br> Hospitals : {}'.format(state,hosp) for state,hosp in zip(states,hospitals)],
                             marker_color='#50d890',hoverinfo = 'text',mode='markers',marker_size=15),1,1)
    fig.add_trace(go.Scatter(x=data['Total_Beds']/100,y=data['Deceased'],text=['State : {} <br> Hospitals : {}'.format(state,hosp) for state,hosp in zip(states,hospitals)],
                             marker_color='#ff2e63',hoverinfo = 'text',mode='markers',marker_size=15),1,1)
    
    fig.update_xaxes(title_text="People/Hospital (in millions)", range = [0,300],row=1, col=2)
    fig.update_yaxes(title_text="Area/Hospital (in 1000 sq km)", range=[0, 80], row=1, col=2)
    fig.update_xaxes(title_text="Hospital Beds (in 100)",range=[0,450],row=1, col=1)
    fig.update_yaxes(title_text="Number of Patients",range=[0,450],row=1, col=1)
    fig.update_layout(
        title="Hospitals and Patient's Status",
        font=dict(
            family="Courier New, monospace"),
    showlegend=False
    )
    
    return fig 

def plot2(path):

    data = get_quadrantplot_data(path)

    fig = make_subplots(rows=1,cols=2)
    
    states = data['State'].values.tolist()
    positive = data['Positive'].values.tolist()
    
    fig.add_trace(go.Scatter(x=data['People/Lab'],y=data['Area/Lab'],text=['State : {} <br> Positive : {}'.format(state,pos) for state,pos in zip(states,positive)],
                             hoverinfo = 'text',mode='markers',marker=dict(size=15,color=data['Positive'],showscale=True)),1,2)
    

    fig.add_shape(
        type='rect',
        x0=0,y0=0,x1=10,y1=1750,xref='x2',
        fillcolor='#64e291',
        opacity=0.3
    )
    
    fig.add_shape(
        type='rect',
        x0=10,y0=0,x1=20,y1=1750,xref='x2',
        fillcolor='#e6e56c',
        opacity=0.3
    )
    
    fig.add_shape(
        type='rect',
        x0=0,y0=1750,x1=10,y1=3500,xref='x2',
        fillcolor='#e6e56c',
        opacity=0.3
    )
    
    fig.add_shape(
        type='rect',
        x0=10,y0=1750,x1=20,y1=3500,xref='x2',
        fillcolor='#eb7070',
        opacity=0.3
    )
    
    data.dropna(inplace=True)
    states = data['State'].values.tolist()
    labs = data['Labs'].values.tolist()
    data['Samples'] = data['Samples']/10
    fig.add_trace(go.Scatter(x=data['Samples'],y=data['Positive'],text=['State : {} <br> Labs : {}'.format(state,lab) for state,lab in zip(states,labs)],
                             marker_color='#0779e4',hoverinfo = 'text',mode='markers',marker_size=15),1,1)
                             
    fig.add_shape(
        type='rect',
        x0=0,y0=0,x1=1750,y1=1750,
        fillcolor='#e6e56c',
        opacity=0.3
    )
    
    fig.add_shape(
        type='rect',
        x0=1750,y0=0,x1=3500,y1=1750,
        fillcolor='#64e291',
        opacity=0.3
    )
    
    fig.add_shape(
        type='rect',
        x0=0,y0=1750,x1=1750,y1=3500,
        fillcolor='#eb7070',
        opacity=0.3
    )
    
    fig.add_shape(
        type='rect',
        x0=1750,y0=1750,x1=3500,y1=3500,
        fillcolor='#e6e56c',
        opacity=0.3
    )
    
    fig.update_xaxes(title_text="People/Lab (in millions)", range = [0,20],row=1, col=2)
    fig.update_yaxes(title_text="Area/Lab (in 1000 sq km)", range=[0, 100], row=1, col=2)
    fig.update_xaxes(title_text="Samples Tested (in 10)",range=[0,3500], row=1, col=1)
    fig.update_yaxes(title_text="Positive Patients",range=[0,3500], row=1, col=1)
    fig.update_layout(
        title='Labs and Tests',
        font=dict(
            family="Courier New, monospace"),
    showlegend=False
    )
    
    return fig 

