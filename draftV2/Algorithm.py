import math
import numpy as np
from collections import defaultdict

time_series_expectedValue = defaultdict(float)
time_series_expected = defaultdict(list)
time_series_currentHour = defaultdict(int)
time_series_lastMaxValue = defaultdict(int)
time_series_lastMaxPosition = defaultdict(int)
decayFunction_values = []

time_series_lastReportedRareEdge = defaultdict(int)
time_series_lastRareEdgePosition = defaultdict(int)

class Algorithm():

    # Polynomial regressions (polynomial least squares fittings).
    def decayFunction(self, TSLRE):
        return (-0.04448 * (TSLRE / 24)) + 3.6  # Generalize better than order 2

    currentHour = -1  # 0 in first iteration
    trainingTime = 30 * 24

    # Cumulative values since Last Rare Edge
    lastMaxValue = 0
    lastMaxValuePosition = 0
    lastTick = 0  # Test
    lastReportedRareEdge = 0

    def feed(s, key, tick):

        # s.cumulativeValues.append(tick)
        avg = 0  # np.mean(s.cumulativeValues[-24:]) --- uncommented
        std = 0  # np.std(s.cumulativeValues[-200:]) --- uncommented

        # Training first 30 days
        time_series_currentHour[key] = time_series_currentHour[key] + 1
        s.currentHour = time_series_currentHour[key]

        if s.currentHour < s.trainingTime:
            time_series_lastMaxValue[key] = max(time_series_lastMaxValue[key], tick)
            # s.lastMaxValue = time_series_maxValues[key]
            time_series_expected[key].append(0)  # UI
            # print('Training ', key, s.currentHour)
            return

        elif s.currentHour == s.trainingTime:

            time_series_lastMaxValue[key] = max(time_series_lastMaxValue[key], tick)
            time_series_lastMaxPosition[key] = s.trainingTime
            time_series_expectedValue[key] = (s.decayFunction(1) * time_series_lastMaxValue[key])  ## working ?
            time_series_expected[key].append(time_series_expectedValue[key])  # UI
            print('Training Completed!!')
            return

        # Time Since Last Rare Edge
        TSLMV = s.currentHour - time_series_lastMaxPosition[key]
        TSLRE = s.currentHour - time_series_lastReportedRareEdge[key]

        if s.currentHour == 1000:
            print("One Thousand")
            print('Analyzing ', key, s.currentHour)
        if s.currentHour == 2000:
            print("Two Thousand")
            print('Analyzing ', key, s.currentHour)
        if s.currentHour == 3000:
            print("Three Thousand")
            print('Analyzing ', key, s.currentHour)
        if s.currentHour == 4000:
            print("Four Thousand")
            print('Analyzing ', key, s.currentHour)
        if s.currentHour == 5000:
            print("Five Thousand")
            print('Analyzing ', key, s.currentHour)


        if tick > time_series_expectedValue[key]:
            if (TSLRE > 24):
                print("*************************** ALERT: ", key)
                print("*************************** Hour: ", s.currentHour, " ----> Value: ", int(tick))
                time_series_lastReportedRareEdge[key] = s.currentHour

        if (s.decayFunction(TSLMV) * time_series_lastMaxValue[key]) < s.decayFunction(1) * tick:
            time_series_expectedValue[key] = s.decayFunction(1) * tick
            time_series_expectedValue[key] = time_series_expectedValue[key] + std
            time_series_lastMaxPosition[key] = s.currentHour
            time_series_lastMaxValue[key] = tick
        else:
            time_series_expectedValue[key] = s.decayFunction(TSLMV) * time_series_lastMaxValue[key]
            time_series_expectedValue[key] = time_series_expectedValue[key] + std

        time_series_expected[key].append(time_series_expectedValue[key])
