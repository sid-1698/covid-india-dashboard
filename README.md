# COVID 19 India Viz #
### This script offers wide range of plots  covering various aspects of  the pandemic in India ###
#### 1. Timeseries Plot : Total cases vs time is plotted to understand the exponential growth of the virus ####
#### 2. Trajectory Plot : This is a very important plot which can help us find out whether we're winning the war or not ####
#### 3. Daily Cases Plot : Daily status is plotted against time. "Flatten the curve" ####
#### 4. Demographics : Age,Tranmission Type,Sex of the patient is analyses. *Most data is missing ####
#### 5. Deepdive : Quadrant plot to analyze why certain states are failing with testing and controlling the pandemic ####
#### 6. Geoplot : State and distrct wise geographic heatmap of number of caes. This will help us to understand the target zones ####

## State Code ##

| Code | State | Code | State |
| ---- | ---- | ---- | ---- |
| AN | Andaman and Nicobar Islands | AP | Andhra Pradesh |
| AR | Arunachal Pradesh | AS | Assam |
| BR | Bihar | CH | Chandigarh |
| CT | Chhattisgarh | DN | Dadra and Nagar Haveli |
| DD | Daman and Diu | DL | Delhi |
| GA | Goa | GJ | Gujarat |
| HR | Haryana | HP | Himachal Pradesh |
| IN | India | JK | Jammu and Kashmir |
| JH | Jharkhand | KA | Karnataka |
| KL | Kerala | LA | Ladakh |
| LD | Lakshadweep | MP | Madhya Pradesh |
| MH | Maharashtra | MN | Manipur |
| ML | Meghalaya | MZ | Mizoram |
| NL | Nagaland | OR | Odisha |
| PY | Puducherry | PB | Punjab |
| RJ | Rajasthan | SK | Sikkim |
| TN | Tamil Nadu | TG | Telangana |
| TR | Tripura | UP | Uttar Pradesh |
| UT | Uttarakhand | WB | West Bengal |

### To run the scipt ###
**Create a Kaggle api and store the json in local users .kaggle**
 Follow this link to know about it : https://github.com/Kaggle/kaggle-api

1. Install all the required packages from requirements.txt
2. First update your database by python scraper.py 
3. View the graph of your interest by python main.py "plontname" "statecode" 

Valid plot names are 
1. Timeseries
2. Trajectory
3. DailyCases
4. Demography
5. Deepdive
6. Geoplot

Credits to https://www.kaggle.com/sudalairajkumar/covid19-in-india and https://www.mohfw.gov.in/ for the dataset. 

## Future Work ##
1. SIR Modelling.
2. Sentiment Analysis using Google Trends. 
3. What is the effect of Lockdown (I feel it's very early to look into it's benefits)
