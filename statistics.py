import pandas as pd
from pathlib import Path
import os 

path = Path(os.path.dirname(os.path.abspath(' '))) / "Data/"
data = pd.read_csv(path/'states_daily.csv',index_col=0)

cases = data[data['status'] == 'Confirmed']['India'].sum()
recoveries = data[data['status'] == 'Recovered']['India'].sum()
deaths = data[data['status'] == 'Deceased']['India'].sum()
