class Algorithm():
    
    # Variables
    _trackAllSpikesValue = []
    _trackAllSpikesPosition = []
    trainingTime = 30 * 24
    
    # Results       
    rareEdgesTrack = {
                        'positions': [], 
                        'values': [], 
                        'reported': []
                    }
    
    # Initialized with the Timeserie
    def __init__(self, timeseries, decay): 
        self.ts = timeseries
        self.decay = decay
    
    # Training first 30 days
    def learnFirst30Days(self):
        self.timeSerieHours = len(self.ts)
        assert self.timeSerieHours > 30, "not enough data"
        self.rareEdgesTrack['positions'].append(self.trainingTime - 1)
        self.rareEdgesTrack['values'].append(np.amax(self.ts[:self.trainingTime]))
        self.rareEdgesTrack['reported'].append(False)
        self._trackAllSpikesValue.append(np.amax(self.ts[:self.trainingTime]))
        self._trackAllSpikesPosition.append(self.trainingTime - 1)
        return
    
    # Polynomial regressions (polynomial least squares fittings).
    def decayFunction(self, TSLRE):
        return (-0.04448 * (TSLRE/24)) + 3.5 if TSLRE/24 < 60 else float('inf') # Generalize better than order 2
#       return (0.0006430209079 * (TSLRE/24)**2) - (0.1041791699 *(TSLRE/24)) + 4.872672204 if TSLRE/24 < 60 else float('inf')
     
    
    # Algorithm    
    def rareEdge_detection(self):

        #State Variables (Online Version)
        state_mean = 0
        
        # Training & Detection
        for i in range(self.trainingTime, self.timeSerieHours):

            # Non-zeros
            tick = self.ts[i]
            if tick == 0:
                continue

            TSLRE = i - self.rareEdgesTrack['positions'][-1] #Time Since Last Rare Edge
            lastRE = self.rareEdgesTrack['values'][-1]  #Last Rare Edge value
            dFactor = self.decay
            
            # Reset Flags
            flag = False
            toReport = False
            
            # Candidate to be a rare edge
            if self.decayFunction(TSLRE) * lastRE < tick:
                toReport = True
            
            # Tracking rare edges
            if toReport or tick > lastRE:
                self.rareEdgesTrack['values'].append(tick)
                self.rareEdgesTrack['positions'].append(i)
        
            # More heuristics for false positives:
            if toReport:
                
                # Learning (24 hours after an rare edge, these are tracked but no re-reported)
                if (TSLRE < 24 and lastRE < tick):
                    toReport = False

                # Rare edges should be 3x greater than the mean of the spikes after the last rare edge was detected
                if tick < (np.mean([value for posValue, value in enumerate(self._trackAllSpikesValue) if self._trackAllSpikesPosition[posValue] < TSLRE])) * 3:
                    toReport = False

                # Rare edges should be 1.5x greater than greatest spike after last last rare edge 
                theValues = [self._trackAllSpikesValue[index] for index, position in enumerate(self._trackAllSpikesPosition) if position < TSLRE]
                if len(theValues) > 0 and tick < np.max(theValues) * 1.50:
                    toReport = False
                    
                # Report here
                self.rareEdgesTrack['reported'].append(toReport)
            
            # A spike is at least 75% of the last of rare edge
            if tick > lastRE * 0.75:
                self._trackAllSpikesValue.append(tick)
                self._trackAllSpikesPosition.append(i)
            
            
        return self.rareEdgesTrack   
       
       
       
# Run Algo    
algoInstance = Algorithm(time_series, 0.5) #Hyperparemeter 0-1
algoInstance.learnFirst30Days()
rareEdgesTrack = algoInstance.rareEdge_detection()


# Print Results
print()
for i in range(len(rareEdgesTrack['reported'])):
    if rareEdgesTrack['reported'][i]:
        print("Rare Edge at ",rareEdgesTrack['positions'][i]," hour: ", rareEdgesTrack['values'][i], " connections")
