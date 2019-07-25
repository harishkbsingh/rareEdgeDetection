import math
import numpy as np
from collections import defaultdict

time_series_expected = defaultdict(list)
time_series_counter = defaultdict(int)
decayFunction_values = []


class Algorithm():

    # Initialized with the Timeserie
    def __init__(self):
        self.hyperparam = None
        self.reset()
        #         time_series_expected = []
        self.cumulativeValues = []
        self.previousExpected = 0

    # Polynomial regressions (polynomial least squares fittings).
    def decayFunction(self, TSLRE):
        return (-0.04448 * (TSLRE / 24)) + 3.6  # Generalize better than order 2

    def secondDecayFunction(self, lastTick, value):
        return abs(lastTick - value)

    def reset(s):
        s.meanSinceLastRareEdge = 0
        s.stdSinceLastRareEdge = 0
        s.timeSinceLastRareEdge = 0
        s.expectedValue = 0

    currentHour = -1  # 0 in first iteration
    trainingTime = 30 * 24

    # Cumulative values since Last Rare Edge
    lastMaxValue = 0
    lastMaxValuePosition = 0
    lastTick = 0  # Test
    lastReportedRareEdge = 0

    def feed(s, key, tick):

        s.cumulativeValues.append(tick)
        avg = 0  # np.mean(s.cumulativeValues[-24:]) --- uncommented
        std = 0  # np.std(s.cumulativeValues[-200:]) --- uncommented

        # Training first 30 days
        time_series_counter[key] = time_series_counter[key] + 1
        s.currentHour = time_series_counter[key]

        if s.currentHour < s.trainingTime:
            s.lastMaxValue = max(s.lastMaxValue, tick)
            time_series_expected[key].append(0)  # UI
            # print('Training ', s.currentHour)
            return

        elif s.currentHour == s.trainingTime:

            s.lastMaxValue = max(s.lastMaxValue, tick)
            s.lastMaxValuePosition = s.trainingTime
            s.expectedValue = (s.decayFunction(1) * s.lastMaxValue)  ## working ?
            s.previousExpected = s.expectedValue
            time_series_expected[key].append(s.expectedValue)  # UI
            # print("*************************** Key: ", key)
            print('Training Completed!!')
            return

        # Time Since Last Rare Edge
        TSLMV = s.currentHour - s.lastMaxValuePosition
        TSLRE = s.currentHour - s.lastReportedRareEdge
        # print('Analyzing ', s.currentHour)

        if s.currentHour == 1000:
            print("One Thousand")
        if s.currentHour == 2000:
            print("Two Thousand")
        if s.currentHour == 3000:
            print("Three Thousand")
        if s.currentHour == 4000:
            print("Four Thousand")
        if s.currentHour == 5000:
            print("Five Thousand")


        if tick > s.expectedValue:
            if (TSLRE > 24):
                print("*************************** ALERT: ", key)
                print("*************************** Hour: ", s.currentHour, " ----> Value: ", int(tick))
                lastReportedRareEdge = s.currentHour

        if (s.decayFunction(TSLMV) * s.lastMaxValue) < s.decayFunction(1) * tick:
            s.expectedValue = s.decayFunction(1) * tick
            s.expectedValue = s.expectedValue + std
            s.lastMaxValuePosition = s.currentHour
            s.lastMaxValue = tick
        else:
            s.expectedValue = s.decayFunction(TSLMV) * s.lastMaxValue
            s.expectedValue = s.expectedValue + std

        time_series_expected[key].append(s.expectedValue)
