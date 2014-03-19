#!/usr/bin/python
#for command line arguments
import argparse
#mostly for debugging data structures
import pprint
#for calculating standard devations
from math import sqrt
#histograms
import matplotlib.pyplot as plt
#Import the labview loader
import sys 
sys.path.append("../../common")
import labviewloader 
#Arbitrary precision decimals
import decimal
#Directory creation
import os
import errno
#filename manipulation
import re
#Power law fitting by maximum likelihood
import plfit



#A skeleton statistic gatherer that just prints values
class StatisticGatherer:
    def __init__(self):
        self.channel = None
        pass
    
    def setChannel(self, channel):
        self.channel = channel
        
    def update(self, timestamp, value):
        print channel, timestamp, value
    
    def report(self):
        print "Report!"

#A statistic gatherer that detects spikes in each channel,
#and reports spike times and inter-spike timing histograms
class SpikeStatGatherer:
    def __init__(self):
        self.channel = None
        self.allData = []
        self.total = 0
        self.sumOfSquares = 0
        self.mean = 0
        self.stdDev = 0
        self.channelSummaries = {}
        self.threshScale = 3
        
    def setChannel(self, channel):
        if self.channel is not None:
            self.mean = self.total/len(self.allData)
            self.stdDev = sqrt((self.sumOfSquares/len(self.allData) - self.mean * self.mean))
            spikes = []
            startedSpike = False
            tStart = 0
            tEnd = 0
            #Find all the spikes, and record their start and end times
            for sample in self.allData:
                if (sample[2] > self.mean + decimal.Decimal(self.stdDev * self.threshScale) or sample[2] < self.mean - decimal.Decimal(self.stdDev * self.threshScale)) and not startedSpike:
                    #Crossed threshold, and not already in a spike
                    tStart = sample[1]
                    startedSpike = True
                elif startedSpike:
                    #A spike started, but now is over, record endtime
                    tEnd = sample[1]
                    spikes.append((tStart, tEnd))
                    startedSpike = False
            #Get a list of inter-spike timings
            gaps = []
            for index in range(1, len(spikes)):
                gap = spikes[index][0] - spikes[index-1][0]
                gaps.append(gap)
            axes = zip(*self.allData)
            
            #Fit the list of inter-spike timing to a power law distribution
            #Only do it if there ARE enough inter-spike timings
            pLaw = [0,0,0]
            
            if len(gaps) > 0: 
                try:
                    pLaw = plfit.plfit(gaps, 'finite')
                except ValueError:
                    print "VALUE ERROR fitting power law to {0} points".format(len(gaps))
                    plaw = [0,0,0]
            else:
                pLaw = [0,0,0]
            #Save the summary
            self.channelSummaries[channel] = [self.mean, self.stdDev, spikes, gaps, axes[1], axes[2], pLaw]
            
        #Reset everything
        self.channel = channel
        self.allData = []
        self.total = 0
        self.sumOfSquares = 0
        self.mean = 0
        self.stdDev = 0
        
    def update(self, timestamp, value):
    	#print "Debug: value=" + str(value) + '\n'
        try:
            self.allData.append((self.channel, timestamp, float(value)))
        except TypeError:
            print value
            
        #Accumulate values for standard deviation and mean
        self.sumOfSquares += value * value
        self.total += value
        
    def report(self, dir_name):
        
        #Ensure that directory exists
        try:
            os.makedirs(dir_name)
        except OSError as exception:
            #Ignore the error case of the dir already existing
            if exception.errno != errno.EEXIST:
                raise
            
        with open("{0}/stats.html".format(dir_name), 'w') as outfile:
            outfile.write('''<html>
            <head>
            </head>
            <body>
            ''')
            for key in self.channelSummaries.keys():
                outfile.write("Channel {0}<br />\n".format(key))
                outfile.write("Mean: {0}<br />\n".format(self.channelSummaries[key][0]))
                outfile.write("Std. Dev.: {0}<br />\n".format(self.channelSummaries[key][1]))
                outfile.write("Spike count: {0}<br />\n".format(len(self.channelSummaries[key][2])))
                outfile.write("Scaling exponent: {0}<br />\n".format(self.channelSummaries[key][6][0]) )
                #Spikes per second, assuming 1k samples per second
                outfile.write("Spike rate in spikes/second: {0}\n".format((float(len(self.channelSummaries[key][2]))/len(self.channelSummaries[key][5]))*1000))
                
                #Graph a histogram of the spike counts, assuming there were any. 
                #It is possible that no spikes were logged on a channel, but unlikely.
                if len(self.channelSummaries[key][3]) > 0:
                    plt.hist(self.channelSummaries[key][3], bins=100)
                    plt.ylabel("Count")
                    plt.xlabel("Inter-spike interval")
                    imgPath = "SpikeHistogramCh{0}.png".format(key)
                    outfile.write("<img src=\"{0}\"<br />\n".format(imgPath))
                    imgPath = "{0}/{1}".format(dir_name, imgPath)
                    plt.savefig(imgPath)
                    plt.close()
                
                #Graph the actual activity
                #The zip call creates a list of all timestamps and a list of all voltages
                plt.plot(self.channelSummaries[key][4],self.channelSummaries[key][5])
                fig = plt.gcf()
                fig.set_figwidth(16)
                plt.axhline(self.channelSummaries[key][0] + decimal.Decimal(self.channelSummaries[key][1]*self.threshScale), color='red', label="spike threshold")
                plt.axhline(self.channelSummaries[key][0] - decimal.Decimal(self.channelSummaries[key][1]*self.threshScale), color='red', label="spike threshold")
                plt.xlabel("Seconds")
                plt.ylabel("Volts")
                imgPath = "VoltageOverTimeCh{0}.png".format(key)
                outfile.write("<img src=\"{0}\"<br />\n".format(imgPath))
                imgPath = "{0}/{1}".format(dir_name, imgPath)    
                plt.savefig(imgPath)
                plt.clf()
                
                
                outfile.write("<br />")
            outfile.write('''
            </body>
            ''')
            outfile.close()
            
        
if __name__ == '__main__':
    #Get the file name
    ap = argparse.ArgumentParser(description="Load a labview file and characterize the channels")
    #ap.add_argument('-s', help='Detect spikes instead of bursts', action='store_true')
    ap.add_argument('fname', help='File name to parse')

    args = ap.parse_args()
    
    #Load a labview datafile
    print "Loading {0}...".format(args.fname),
    Ll = labviewloader.LabViewLoader()
    Ll.load(args.fname)
    print "done."
    
    #Get the directory name for the output
    name_base = os.path.split(args.fname)[1].split('.')[0]
    saveName = "./stats_{0}".format(name_base)
    #Set up a list of statistic gatherers
    #TODO configure this based on command line options
    gatherers = [SpikeStatGatherer()]
    
    #Get the columns and rows
    columns = int(Ll.getHeaderValue("Channels", 1))
    samples = int(Ll.getHeaderValue("Samples", 1))
    #Time step between each sample
    deltaT = float(Ll.getHeaderValue("Delta_X", 1))
    
    #Go through all the data and pass it off to the statistic gatherers
    #Iterate the columns
#
    for channel in xrange(0, columns):
        #Inform all statistic gatherers that we changed channel
        for gatherer in gatherers:
            gatherer.setChannel(channel)
        #Iterate the data in each column
        data = Ll.getDataCol(channel)
        
        #THROW AWAY THE FIRST HALF SECOND
        #NOTE THIS IS A HACK TO GET AROUND ELECTRICAL 
        #ISSUES IN THE MEA SENSOR HARDWARE
        data = data[500:]
        timestamp = 0.005
        
        for datum in data:
            #Update all the gatherers with the value
            for gatherer in gatherers:
                gatherer.update(timestamp, datum)
            #Next timestamp
            timestamp = timestamp + deltaT
    
    #Gather the reports from the statistic gatherers
    for gatherer in gatherers:
        gatherer.report(saveName)
