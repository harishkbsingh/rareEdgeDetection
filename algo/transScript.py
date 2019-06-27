# file = 'wgetthinkbroadband_hourGrouping.csv'
# file = 'datacollectorr_amazon_hourGrouping.csv'
# file = 'curltxt_hourGrouping.csv'
# file = 'datacollectorr_hourGrouping.csv'
# file = 'Snowflake_dayGrouping.csv'
file = 'threatsolver_snowflakecomputing.csv'
# file = 'javanet.lacework.threatresolver.Main_amazonawscom.csv'


#Custom function to generate missing entries in the time serie 
import datetime
import collections
import numpy as np

# base = datetime.datetime.today()
base = datetime.datetime(2019, 1, 1)
date_list = [base + datetime.timedelta(hours=x) for x in range((24*30*5) + 13)]
di = collections.defaultdict(int)
for t in date_list:
#     print(t.strftime("%Y-%m-%d %H:%M:%S.000"))
    di[t.strftime("%Y-%m-%d %H:%M:%S.000")] = 0
    

with open('datasets_byhour_raw/'+file) as f:
    ts_array = f.readline()
    ts_array = f.readlines()
def transform(ts_str):
    entity_dict = {}
    temp_array = ts_str.split(',')
    date =  temp_array[0]
    di[date] = float(temp_array[3])  
#     return di

for x in ts_array:
    transform(x)
    
# we want to save it to open it with JMP and visualize it easier.
time_series = list(di.values())
# np.savetxt('datasets_byhour/'+file, time_series, delimiter=',')
