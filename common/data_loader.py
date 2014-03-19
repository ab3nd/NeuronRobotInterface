#!/usr/bin/python

import labviewloader
import csv

class data_loader:

    def __init__(self):
        self.channels = None
        self.samples = None
        self.deltaT = None
        self.data = None
            
    def load(self, fName):
        # Handle CSV file
        if fName.endswith(".csv"):
            self.channels = 60
            self.samples = 0
            self.deltaT = 0.001
            self.data = [[] * channels]
            # Assemble the columns, each column is one channel
            with open(fName) as infile:
                reader = csv.read(infile, delimiter=",", quoting=csv.QUOTE_NONE)
                for row in reader:
                    for ii in range(0, channels):
                        self.data[ii].append(float(row[ii]))
                    #Count rows
                    self.samples += 1
                    
        else:
            # Load a labview file
            ll = labviewloader.LabViewLoader()
            ll.load(fName)
        
            # Load the parameters from the file
            self.channels = int(ll.getHeaderValue("Channels", 1))
            self.samples = int(ll.getHeaderValue("Samples", 1))
            self.deltaT = float(ll.getHeaderValue("Delta_X", 1))
        
            # collect all the data as floats
            self.data = []
            for channel in range(0, self.channels):
                temp = ll.getDataCol(channel)
                accumulator = []
                for value in temp:
                    accumulator.append(float(str(value)))
                self.data.append(accumulator)
            
    def getChannel(self, channel):
        return self.data[channel]
    
    def getAllChannels(self):
        return self.data
    
    def getSamples(self):
        return self.samples

    def getDeltaT(self):
        return self.deltaT