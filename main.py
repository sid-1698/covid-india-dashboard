import scraper
from pathlib import Path
import sys
import os


import tsplot
import trajplot
import dailycases
import demographics
import deepdive
import geoplot

def view_plot(path,plot,state):

    fig2 = None
    jsonpath = path/'GeoJson/'

    if plot == 'timeseries':
        if len(state) > 1:
            print("Timeseries plot can be plotted for only one state")
            return 0
        fig = tsplot.plot(path,state[0])

    elif plot == 'trajectory':
        fig = trajplot.plot(path,state)
    
    elif plot == 'dailycases':
        if len(state) > 1:
            print("Please view one state at a time. Will fix the issue soon")
            return 0
        fig = dailycases.plot(path,state[0])
    
    elif plot == 'demography':
        if ((state[0] != 'IN') | (len(state) != 1)):
            print("Statewise demographic data is unavailable. But take a loot at nation wide data")
        fig = demographics.plot1(path)
        fig2 = demographics.plot2(path)
    
    elif plot == 'deepdive':
        if ((state[0] != 'IN') | (len(state) != 1)):
            print("Districtwise analysis is unavailable. But take a loot at statewise data") 
        fig = deepdive.plot1(path)
        fig2 = deepdive.plot2(path)
    
    elif plot == 'geoplot':
        fig = geoplot.plot1(path,jsonpath)
        if len(state) > 1:
            print("Please view one state at a time. Will fix the issue soon")
            return 0
        fig2 = geoplot.plot2(path,jsonpath,state[0])
    
    fig.show()
    if fig2 == None:
        print("Thanks for Viewing")
    else:
        fig2.show()
        print("Thanks for Viewing")
        
def main(path,argv):
    code = {'mh': 'Maharashtra','dl': 'Delhi','tn': 'Tamil Nadu','mp': 'Madhya Pradesh','rj': 'Rajasthan','gj': 'Gujarat','up': 'Uttar Pradesh',
              'tg': 'Telangana','ap': 'Andhra Pradesh','kl': 'Kerala','ka': 'Karnataka','jk': 'Jammu and Kashmir','wb': 'West Bengal',
              'hr': 'Haryana','pb': 'Punjab','br': 'Bihar','or': 'Odisha','ut': 'Uttarakhand','hp': 'Himachal Pradesh','as': 'Assam',
              'ct': 'Chhattisgarh','jh': 'Jharkhand','ch': 'Chandigarh','la': 'Ladakh','an': 'Andaman and Nicobar Islands','ga': 'Goa',
              'py': 'Puducherry','ml': 'Meghalaya','mn': 'Manipur','tr': 'Tripura','mz': 'Mizoram','ar': 'Arunachal Pradesh',
              'dn': 'Dadra and Nagar Haveli','nl': 'Nagaland','dd': 'Daman and Diu','ld': 'Lakshadweep','sk': 'Sikkim','in' :'India'}

    plotname = argv[1].lower()
    state = ['in']
    if len(argv)>2:
        if ',' not in argv[2]:
            state = [argv[2].lower()]
        else:
            state = argv[2].split(',')
            state = [item.lower() for item in state]

    if plotname not in ['timeseries','trajectory','dailycases','demography','deepdive','geoplot']:
        print("Invalid Plot Name. Please Choose one from")
        print(['timeseries','trajectory','dailycases','demography','deepdive','geoplot'])
        return 0
    
    for i,st in enumerate(state):
        if st not in code.keys():
            print(st,"Inavlid Code. Please Enter a valid state code. Refer README for state codes")
            return 0
        state[i] = code[st]
        
    
    view_plot(path,plotname,state)

if __name__ == "__main__":
    path = Path(os.path.dirname(os.path.abspath(' '))) / "Data/"
    main(path,sys.argv)  