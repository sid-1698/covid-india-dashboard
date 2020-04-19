import requests
import json
import pandas as pd 
import numpy as np
import os
import sys
import warnings
import datetime 
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns',None)

api = KaggleApi()
api.authenticate()

def testing_data(path):
    
    if os.path.exists(path/'StatewiseTestingDetails.csv'):
        os.remove(path/'StatewiseTestingDetails.csv')
    api.dataset_download_file('sudalairajkumar/covid19-in-india','StatewiseTestingDetails.csv',path=path)
    data = pd.read_csv(path/'StatewiseTestingDetails.csv')
    data['Date'] = pd.to_datetime(data['Date'],format='%Y-%m-%d')
    data = data[['Date','State','TotalSamples','Positive']]
    data.columns = ['Date','State','Samples','Positive']

    data.to_csv(path/'StatewiseTestingDetails.csv')

def hospitals_data(path):
    
    if os.path.exists(path/'HospitalBedsIndia.csv'):
        os.remove(path/'HospitalBedsIndia.csv')
        
    api.dataset_download_file('sudalairajkumar/covid19-in-india','HospitalBedsIndia.csv',path=path)
    data = pd.read_csv(path/'HospitalBedsIndia.csv')
    data = data[['State/UT','NumRuralHospitals_NHP18','NumRuralBeds_NHP18',
                                   'NumUrbanHospitals_NHP18','NumUrbanHospitals_NHP18']]
    data.columns = ['State','RH','RB','UH','UB']
    data['Total_Beds'] = data.apply(lambda row : row['RB'] + row['UB'],axis=1)
    data['Total_Hospitals'] = data.apply(lambda row : row['RH'] + row['UH'],axis=1)
    data.to_csv(path/'HospitalBedsIndia.csv')

def labs_data(path):
    
    if os.path.exists(path/'ICMRTestingLabs.csv'):
        os.remove(path/'ICMRTestingLabs.csv')
    
    api.dataset_download_file('sudalairajkumar/covid19-in-india','ICMRTestingLabs.csv',path=path)

def population_data(path):
    
    if os.path.exists(path/'population_india_census2011.csv'):
        os.remove(path/'population_india_census2011.csv')
    
    api.dataset_download_file('sudalairajkumar/covid19-in-india','population_india_census2011.csv',path=path)
    data = pd.read_csv(path/'population_india_census2011.csv')
    data = data[['State / Union Territory','Population','Area','Density','Gender Ratio']]
    data.columns = ['State','Population','Area','Density','Ratio']
    data['Density'] = data['Density'].apply(lambda x : float(x.split('/')[0].replace(',','')))
    data['Area'] = data['Area'].apply(lambda x : float(x.split('km')[0].replace(',','')))

    data.to_csv(path/'population_india_census2011.csv')

def get_json_data(api):
    
    response = requests.get(api)
    if response.status_code != 200:
        raise Exception("Unable to Fetch information. Status Code was " + str(response.status_code))
    response = response.text
    json_data = json.loads(response)
    
    return json_data

def states_data(path,code):
    
    json_data = get_json_data('https://api.covid19india.org/states_daily.json')
    data = pd.DataFrame.from_dict(json_data['states_daily'])
    data['date'] = pd.to_datetime(data['date'],format='%d-%b-%y')
    for col in data.columns:
        if ((col != 'date') & (col != 'status')):
            data[col] = pd.to_numeric(data[col],errors='coerce')
    
    data.columns = [code[col] if col in code.keys() else col for col in data.columns]
    
    data.to_csv(path/'states_daily.csv')

def raw_data(path):
    
    json_data = get_json_data('https://api.covid19india.org/raw_data.json')
    data = pd.DataFrame.from_records(json_data['raw_data'])
    data = data[['agebracket','backupnotes','currentstatus','dateannounced','gender','nationality','statecode',
                         'statuschangedate','typeoftransmission']]
    data.columns = ['Age','Information','Curr_Status','Test_Date','Gender','Nationality','State_Code','Change_Date','Transmission_Type']
    data['State_Code'] = data['State_Code'].apply(lambda x : x.lower())
    data['Age'] = pd.to_numeric(data['Age'],errors='coerce')
    
    data.to_csv(path/'raw_data.csv')

def district_data(path,state):
    
    json_data = get_json_data('https://api.covid19india.org/state_district_wise.json')
    json_data = json_data[state]['districtData']
    data = pd.DataFrame(columns=['District','Total_Cases','Cases_Today'])
    ind = 0
    for district in json_data.keys():
        data.loc[ind,'District'] = district
        data.loc[ind,'Total_Cases'] = json_data[district]['confirmed']
        data.loc[ind,'Cases_Today'] = json_data[district]['delta']['confirmed']
        ind += 1
    data['Total_Cases'] = pd.to_numeric(data['Total_Cases'],errors='coerce')
    data['Cases_Today'] = pd.to_numeric(data['Cases_Today'],errors='coerce')
    
    state = 'States_Data/' + state + '.csv'
    if os.path.isdir(path/'States_Data/') == False:
        os.makedirs(path/'States_Data/')
    data.to_csv(path/state)

def get_data(path):
    
    states_code = {'mh': 'Maharashtra','dl': 'Delhi','tn': 'Tamil Nadu','mp': 'Madhya Pradesh','rj': 'Rajasthan','gj': 'Gujarat','up': 'Uttar Pradesh',
              'tg': 'Telangana','ap': 'Andhra Pradesh','kl': 'Kerala','ka': 'Karnataka','jk': 'Jammu and Kashmir','wb': 'West Bengal',
              'hr': 'Haryana','pb': 'Punjab','br': 'Bihar','or': 'Odisha','ut': 'Uttarakhand','hp': 'Himachal Pradesh','as': 'Assam',
              'ct': 'Chhattisgarh','jh': 'Jharkhand','ch': 'Chandigarh','la': 'Ladakh','an': 'Andaman and Nicobar Islands','ga': 'Goa',
              'py': 'Puducherry','ml': 'Meghalaya','mn': 'Manipur','tr': 'Tripura','mz': 'Mizoram','ar': 'Arunachal Pradesh',
              'dn': 'Dadra and Nagar Haveli','nl': 'Nagaland','dd': 'Daman and Diu','ld': 'Lakshadweep','sk': 'Sikkim','tt':'India'}
    
    testing_data(path)
    hospitals_data(path)
    labs_data(path)
    population_data(path)
    states_data(path,states_code)
    raw_data(path)
    
    for _,value in states_code.items():
        try:
            district_data(path,value)
        except:
            print(value,' - Unable to get district data')

if __name__ == "__main__":
    path = Path(os.path.dirname(os.path.abspath(' '))) / "Data/"
    get_data(path)