from Util import getStat, saveAlert, saveStat, getDiffInHours, processNextStdDev, getNewStdDevObject, getSourceAndDestinationFromKey
from Config import trainingTime, oneDayAsMinTime

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
        lastEntry = getStat(key)

        # Default New Entry
        newEntry = dict()
        newEntry['firstTimeSeen'] = currentDate if lastEntry['firstTimeSeen'] is 0 else lastEntry['firstTimeSeen']
        newEntry['currentHour'] = 0 if lastEntry['firstTimeSeen'] is 0 else getDiffInHours(currentDate, lastEntry['firstTimeSeen'])
        newEntry['theKey'] = key
        newEntry['theSource'], newEntry['theDestination'] = getSourceAndDestinationFromKey(key)
        newEntry['lastTimeSeen'] = currentDate
        newEntry['expectedValue'] = lastEntry['expectedValue']
        newEntry['lastMaxValue'] = lastEntry['lastMaxValue']
        newEntry['lastMaxPosition'] = lastEntry['lastMaxPosition']
        newEntry['lastRareEdgePosition'] = lastEntry['lastRareEdgePosition']
        newEntry['lastReportedRareEdge'] = lastEntry['lastReportedRareEdge']
        newEntry['currentValue'] = tick
        newEntry['stdDeviationInfo'], stdDev = processNextStdDev(lastEntry['stdDeviationInfo'], tick)
        currentHour = newEntry['currentHour']

        # Training Period
        if currentHour < trainingTime:
            newEntry['lastMaxValue'] = max(lastEntry['lastMaxValue'], tick)
            newEntry['lastMaxPosition'] = trainingTime
            newEntry['expectedValue'] = (s.decayFunction(1) * newEntry['lastMaxValue'])
            saveStat(newEntry)
            return

        # Time since last Rare Edge & Max Value
        TSLMV = currentHour - lastEntry['lastMaxPosition']
        TSLRE = currentHour - lastEntry['lastRareEdgePosition']

        # If rare, store alert
        if tick > lastEntry['expectedValue']:
            if TSLRE > oneDayAsMinTime:
                saveAlert(key, tick, currentHour, currentDate)
                newEntry['lastRareEdgePosition'] = currentHour
                newEntry['stdDeviationInfo'], stdDev = getNewStdDevObject(), 0

        # Det Next expected valued
        if (s.decayFunction(TSLMV) * lastEntry['lastMaxValue']) < s.decayFunction(1) * tick:
            newEntry['expectedValue'] = (s.decayFunction(1) * tick) + stdDev
            newEntry['lastMaxPosition'] = currentHour
            newEntry['lastMaxValue'] = tick
        else:
            newEntry['expectedValue'] = (s.decayFunction(TSLMV) * lastEntry['lastMaxValue']) + stdDev

        saveStat(newEntry)
