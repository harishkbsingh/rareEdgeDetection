import datetime
from Algorithm import Algorithm
from Util import getEdges, getKeyFromSourceAndDestination
import time

'''
This method simulates running the algorithm every one hour for long period by generating
all dates (in this case) for 6 months starting on 1/1/2019.
'''
def runMonthsSimulation():

    instance = Algorithm()
    base = datetime.datetime(2019, 1, 1)
    six_months = (24*30*5) + 13
    date_list = [base + datetime.timedelta(hours=x) for x in range(six_months)]
    for t in date_list:
        runAlgorithm(instance, t)

    print('*************************** Analysis Completed')


'''
Instance called for each edge (source, destination) with connections in the current hour 
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
        instance.feed(getKeyFromSourceAndDestination(row[0], row[1]), row[2], start)

'''
Starting method ** main ** 
'''
if __name__== "__main__":
    start_time = time.time()
    runMonthsSimulation()
    print("--- %s seconds ---" % (time.time() - start_time))
