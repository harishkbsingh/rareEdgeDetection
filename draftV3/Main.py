import datetime
from Algorithm import Algorithm
from Util import getEdges, getKey

'''
This method simulates the algorithm for 6 months
'''
def runMonthsSimulation():

    instance = Algorithm()
    base = datetime.datetime(2019, 1, 1)
    date_list = [base + datetime.timedelta(hours=x) for x in range((24*30*5) + 13)]
    for t in date_list:
        runAlgorithm(instance, t)

    print('*************************** Analysis Completed')

'''
Algorithm ran for each edge (source, destination) in the current hour 
Input: algorithm instance (instance) and current date (date)
Output: None
'''
def runAlgorithm(instance, date):

    # For each edge in given hour: source, dest, #connection
    start = date.strftime("%Y-%m-%d %H:%M:%S")
    end = (date + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    dictionary = getEdges(start, end)

    # Feed algorithm for each edge
    for key, row in dictionary.items():
        instance.feed(getKey(row[0], row[1]), row[2], start)

runMonthsSimulation()