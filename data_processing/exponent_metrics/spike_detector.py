import decimal
import math

def meanAndSD(values):
    sumOfSquares = reduce(lambda sum, val: sum + (val*val), values, 0)
    mean = sum(values)/len(values)
    stDev = math.sqrt((sumOfSquares/len(values) - mean * mean))
    return mean, stDev

class threshSpikeDetector:
    def __init__(self, threshold = 0.0025):
        self.limit = decimal.Decimal(str(threshold))
    
    def update(self, input):
        if decimal.Decimal(str(abs(input))) > self.limit:
            return True
        return False
    
    def isBursting(self):
        print "**NOT IMPLEMENTED**"
        return False 

class spikeDetector:
    def __init__(self):
        #window size is in units of samples
        self.windowSize = 50
        self.samples = []
        self.burstCounter = 0
                        
    def update(self, newVal):
        self.samples.append(abs(newVal))
        if len(self.samples) > self.windowSize:
            self.samples.pop(0)
        
        #Not using this
        #difference = max(self.samples) - min(self.samples)
        
        #Calculate the mean and standard deviation
        mean, stdev = meanAndSD(self.samples)
        
        if abs(newVal) > 3 * decimal.Decimal(str(stdev)):
            self.burstCounter = self.burstCounter + 1
        else:
            self.burstCounter = 0
        
    def isBursting(self):
        if self.burstCounter > 5:
            return True
        else:
            return False

# Buffers the first 30 seconds of data for calculations. 
# This does mean that the detector will not fire for the first 30 seconds
# The buffered data is used to calculate two metrics:
#    Baseline - The average of all samples in the first 30 seconds
#    Standard Deviation - calculated over all samples
# Any sample greater than 3 * SD over baseline is a spike
# Three or more spikes within some time window are a burst
# Returns true if the new sample is a spike.
class bufferingSpikeDetector:
    #Sample step is the time step between samples in seconds, buffer depth is in seconds 
    def __init__(self, sampleStep = 0.001000, bufferDepth = 0.7):
        self.bufferSamples = int(bufferDepth/sampleStep)
        self.buffer = []
        self.burstWindow = [0] * 20
        self.burstCountThreshold = 4
        self.mean = 0  
        self.stdev = 0
        
    def update(self, newSample):
        if len(self.buffer) < self.bufferSamples - 1:
            #Not done buffering yet
            self.buffer.append(newSample)
            return False
        elif len(self.buffer) == self.bufferSamples - 1:
            #Just got last sample, calculate SD and Baseline
            self.buffer.append(newSample)
            self.mean, self.stdev = meanAndSD(self.buffer)
            print "Mean: {0}, Standard Deviation: {1}".format(self.mean, self.stdev)
            return False
        else:
            self.burstWindow.pop(0)
            # 3 standard deviations was big enough to prevent spike detection
            if abs(newSample) > self.mean + decimal.Decimal(str(self.stdev * 1.26)):
                self.burstWindow.append(1)
                return True
            else:
                self.burstWindow.append(0)
                return False
        return False
    
    def isBursting(self):
        #print self.burstWindow
        if sum(self.burstWindow) > self.burstCountThreshold:
            return True
        return False