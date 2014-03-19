#!/usr/bin/python

#Given an lvm or csv file, output the spike rate for each channel.

import sys
sys.path.append("../common")
import data_loader
import spike_detector
import os

# Get the file off the command line 
infile = sys.argv[1]
loader = data_loader.data_loader()
loader.load(infile)

# Get the spike rate for each channel
sd = spike_detector.spike_detector()
channelNum = 1

# Conversion of samples to seconds
runLenSec = loader.getSamples() * loader.getDeltaT()

#Create a filename to save the output to
basename = os.path.basename(infile).split(".")[0]
outFName = "./" + basename + "-spike_rates"

with open(outFName, 'w') as outFile:
    for channel in loader.getAllChannels():
        spikes = sd.channelToSpike(channel)
        outFile.write("{0},{1}\n".format(channelNum, (sum(spikes)/runLenSec)))
        channelNum += 1
        
