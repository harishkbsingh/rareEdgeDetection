class Algorithm():
    
    # Constants 
    trainingTime = 30 * 24
    timeLast60days = 60 * 24
    timeLast30days = 30 * 24
    timeLast15days = 15 * 24
    timeLast5days  = 5 * 24
    timeLast1days  = 24
    timeLast5hours = 5
    
    # Results       
    trackAllSpikesValue = []
    trackAllSpikesPosition = []
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
        self.trackAllSpikesValue.append(np.amax(self.ts[:self.trainingTime]))
        self.trackAllSpikesPosition.append(self.trainingTime - 1)
        return
        
    # Algorithm    
    def rareEdge_detection(self):

        # Initializations
        flag = False
        spike = False
        
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
            
        
            # Heuristics
            if (TSLRE > self.timeLast60days and tick > np.mean(self.rareEdgesTrack['values']) * 0.50) or \
               (TSLRE > self.timeLast30days and TSLRE < self.timeLast60days and lastRE * 1.50 < tick) or \
               (TSLRE > self.timeLast15days and TSLRE < self.timeLast30days and lastRE * 2 < tick) or \
               (TSLRE > self.timeLast5days and TSLRE < self.timeLast15days and lastRE * 3 < tick) or \
               (TSLRE > self.timeLast1days and TSLRE < self.timeLast5days and lastRE * 5 < tick):
                self.rareEdgesTrack['values'].append(tick)
                self.rareEdgesTrack['positions'].append(i)
                toReport = True
            elif tick > lastRE:
                self.rareEdgesTrack['values'].append(tick)
                self.rareEdgesTrack['positions'].append(i)
        
            # More heuristics for false positives:
            if toReport:
                
                # Learning (24 hours after an rare edge, these are tracked but no re-reported)
                if (TSLRE < self.timeLast1days and lastRE < tick):
                    toReport = False

                # Rare edges should be 3x greater than the mean of the spikes after the last rare edge was detected
                if tick < (np.mean([value for posValue, value in enumerate(self.trackAllSpikesValue) if self.trackAllSpikesPosition[posValue] < TSLRE])) * 3:
                    toReport = False

                # Rare edges should be 1.5x greater than greatest spike after last last rare edge 
                theValues = [self.trackAllSpikesValue[index] for index, position in enumerate(self.trackAllSpikesPosition) if position < TSLRE]
                if len(theValues) > 0 and tick < np.max(theValues) * 1.50:
                    toReport = False
                    
                # Report here
                self.rareEdgesTrack['reported'].append(toReport)
            
            # A spike is at least 75% of the last of rare edge
            if tick > lastRE * 0.75:
                self.trackAllSpikesValue.append(tick)
                self.trackAllSpikesPosition.append(i)
            
            
        return self.rareEdgesTrack    
    
    
# Run Algo    
algoInstance = Algorithm(time_series, 0.5) #Hyperparemeter 0-1
# algoInstance = Algorithm(time_series)
algoInstance.learnFirst30Days()
rareEdgesTrack = algoInstance.rareEdge_detection()


# Print Results
print()
for i in range(len(rareEdgesTrack['reported'])):
    if rareEdgesTrack['reported'][i]:
        print("Rare Edge at ",rareEdgesTrack['positions'][i]," hour: ", rareEdgesTrack['values'][i], " connections")
