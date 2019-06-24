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
    def __init__(self, timeseries): 
        self.ts = timeseries
    
    
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

            # Only distance
            if self.ts[i] == 0:
                continue

            # Distance from last Rare Edge (TSLRE = Time Since Last Rare Edge)
            TSLRE = i - self.rareEdgesTrack['positions'][-1]
             
            # Reset Flags
            flag = False
            toReport = False
            
        
            # Heuristics
            if (TSLRE > self.timeLast60days and self.ts[i] > np.mean(self.rareEdgesTrack['values']) * 0.50) or \
               (TSLRE > self.timeLast30days and TSLRE < self.timeLast60days and self.rareEdgesTrack['values'][-1] * 1.50 < self.ts[i]) or \
               (TSLRE > self.timeLast15days and TSLRE < self.timeLast30days and self.rareEdgesTrack['values'][-1] * 2 < self.ts[i]) or \
               (TSLRE > self.timeLast5days and TSLRE < self.timeLast15days and self.rareEdgesTrack['values'][-1] * 3 < self.ts[i]) or \
               (TSLRE > self.timeLast1days and TSLRE < self.timeLast5days and self.rareEdgesTrack['values'][-1] * 5 < self.ts[i]):
                self.rareEdgesTrack['values'].append(self.ts[i])
                self.rareEdgesTrack['positions'].append(i)
                toReport = True
            elif self.ts[i] > self.rareEdgesTrack['values'][-1]:
                self.rareEdgesTrack['values'].append(ts[i])
                self.rareEdgesTrack['positions'].append(i)
        
            # More heuristics for false positives:
            if toReport:
                
                # Learning (24 hours after an rare edge, these are tracked but no re-reported)
                if (TSLRE < self.timeLast1days and self.rareEdgesTrack['values'][-1] < self.ts[i]):
                    toReport = False

                # Rare edges should be 3x greater than the mean of the spikes after the last rare edge was detected
                if self.ts[i] < (np.mean([value for posValue, value in enumerate(self.trackAllSpikesValue) if self.trackAllSpikesPosition[posValue] < TSLRE])) * 3:
                    toReport = False

                # Rare edges should be 1.5x greater than greatest spike after last last rare edge 
                theValues = [self.trackAllSpikesValue[index] for index, position in enumerate(self.trackAllSpikesPosition) if position < TSLRE]
                if len(theValues) > 0 and self.ts[i] < np.max(theValues) * 1.50:
                    toReport = False
                    
                # Report here
                self.rareEdgesTrack['reported'].append(toReport)
            
            # A spike is at least 75% of the last of rare edge
            if self.ts[i] > self.rareEdgesTrack['values'][-1] * 0.75:
                self.trackAllSpikesValue.append(self.ts[i])
                self.trackAllSpikesPosition.append(i)
            
            
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
