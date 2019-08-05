from Util import getStat, saveAlert, saveStat, getDiffInHours, printing, processNextStdDev, getStdDevObject, getSourceAndDestinationFromKey
from Config import trainingTime, oneDayAsMinTime
import ast

class Algorithm():

    """
    Polynomial regressions (polynomial least squares fittings).
    This one generalized better than when testing with order 2
    """
    def decayFunction(self, TSLRE):
        return (-0.04448 * (TSLRE / 24)) + 3.6

    """
    This method processes the # of connection (tick) of an edge(key) in a given 1  hour range (currentDate)  
    Input: key, # of connections, current date
    Output: Compute next expected value
    """
    def feed(s, key, tick, currentDate):

        # Load last edge entry
        entry = getStat(key)

        # New entry to be saved
        toSave = dict()
        toSave['firstTimeSeen'] = currentDate if entry['firstTimeSeen'] is 0 else entry['firstTimeSeen']
        toSave['currentHour'] = 0 if entry['firstTimeSeen'] is 0 else getDiffInHours(currentDate, entry['firstTimeSeen'])
        toSave['theKey'] = key
        toSave['theSource'], toSave['theDestination'] = getSourceAndDestinationFromKey(key)
        toSave['lastTimeSeen'] = currentDate
        toSave['expectedValue'] = entry['expectedValue'] # 0 during training
        toSave['lastMaxValue'] = entry['lastMaxValue']  # 0 during training
        toSave['lastMaxPosition'] = entry['lastMaxPosition'] # 0 # 0 during training
        toSave['lastRareEdgePosition'] = entry['lastRareEdgePosition']
        toSave['lastReportedRareEdge'] = entry['lastReportedRareEdge']
        toSave['currentValue'] = tick
        toSave['stdDeviationInfo'], stdDev = processNextStdDev(entry['stdDeviationInfo'], tick)
        currentHour = toSave['currentHour']

        # Training Period
        if currentHour < trainingTime:
            toSave['lastMaxValue'] = max(entry['lastMaxValue'], tick)
            toSave['lastMaxPosition'] = trainingTime
            toSave['expectedValue'] = (s.decayFunction(1) * toSave['lastMaxValue'])
            saveStat(toSave)
            return

        # Time since last Rare Edge & Max Value
        TSLMV = currentHour - entry['lastMaxPosition']
        TSLRE = currentHour - entry['lastRareEdgePosition']

        printing(currentDate, key) #### Printing

        # If rare, store alert
        if tick > entry['expectedValue']:
            if TSLRE > oneDayAsMinTime:
                saveAlert(key, tick, currentHour, currentDate)
                toSave['lastRareEdgePosition'] = currentHour
                toSave['stdDeviationInfo'], stdDev = getStdDevObject(), 0

        # Det expected valued
        if (s.decayFunction(TSLMV) * entry['lastMaxValue']) < s.decayFunction(1) * tick:
            toSave['expectedValue'] = (s.decayFunction(1) * tick) + stdDev
            toSave['lastMaxPosition'] = currentHour
            toSave['lastMaxValue'] = tick
        else:
            toSave['expectedValue'] = (s.decayFunction(TSLMV) * entry['lastMaxValue']) + stdDev

        saveStat(toSave)
