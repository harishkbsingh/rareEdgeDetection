# Custom function to generate missing entries in the time serie
import datetime
import collections
import numpy as np
from collections import defaultdict
from Algorithm import Algorithm, time_series_expected
from Util import getEdges

def run():

    time_series = defaultdict(list)

    algoInstance = Algorithm()

    # Everyday job
    base = datetime.datetime(2019, 1, 1)
    date_list = [base + datetime.timedelta(hours=x) for x in range((24*30*5) + 13)]
    di = collections.defaultdict(int)
    # time_series = {}
    for t in date_list:
        start = t.strftime("%Y-%m-%d %H:%M:%S")
        end = (t + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        dictionary = getEdges(start, end)
        counter = 0
    #     print(dictionary)
        for key, row in dictionary.items():
            counter = counter + 1
            key = row[0] + '---' + row[1]
            time_series_expected[key].append(row[2]) #for plotting: time serie
    #         print('Processing (#', counter, ') - ', start, ' ',  key, '---', row[2])
            algoInstance.feed(key, row[2])
    print('*************************** Analysis Done')
run()