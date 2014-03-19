#!/usr/bin/python
import numpy as np

class spike_detector:
    def __init__(self):
        pass
    
    #TODO add methods to do spike detection in realtime
    
    def channelToSpike(self, data, threshMult = 3):
        mean = np.average(data)
        stdDev = np.std(data)
        spikes = []
        # Zero-mean the data to make the spike detection easier
        zeroMean = [sample - mean for sample in data]
        thresh = stdDev * 3
        
        #For each sample in the data, determine if it counts as a spike
        for value in data:
            if value > thresh:
                spikes.append(True)
            elif value < (0-thresh):
                spikes.append(True)
            else:
                spikes.append(False)
        
        return spikes            