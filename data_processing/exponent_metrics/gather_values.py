#!/usr/bin/python

#Gather stat values from the various files, save them as CSV files for analysis

import os
import re


#Compile the REs up front for speed, these include a group for the number
reScalExp = re.compile("Scaling exponent: ([0-9\.]+)")
reSpikeRt = re.compile("Spike rate in spikes/second: ([0-9\.]+)")
#For finding information about the file from the name
reSheaDate = re.compile("[0-9][0-9][A-Z][a-z]{2}")

#Try on just one file 
def getScaleSpikeRate(filename):
    with open(filename) as infile:
        line = infile.readline()
        scaleLine = ""
        spikeLine = ""
        while line:
            match = re.match(reScalExp, line)
            if match is not None:
                if scaleLine != "":
                    scaleLine += ","
                scaleLine += "{0}".format(match.group(1))
            match = re.match(reSpikeRt, line)
            if match is not None:
                if spikeLine != "":
                    spikeLine += ","
                spikeLine += "{0}".format(match.group(1))
            line = infile.readline()
        infile.close() 
        return scaleLine, spikeLine

#Open the spike and scaling exponent files
scaleFile = open("./scaleExps.csv", 'w')
spikeFile = open("./spikeRates.csv", 'w')

#Expects to be executed in the metrics directory
for root, dirs, files in os.walk('./'):
    if root.startswith("./stats"):
        #So get the csv values and write the file
        filename = "{0}/stats.html".format(root)
        scales, spikes = getScaleSpikeRate(filename)
        scaleFile.write(root + "," + scales + "\n")
        spikeFile.write(root + "," + spikes + "\n")
        
spikeFile.close()
scaleFile.close()        

#After running, the CSV files can be seperated by type using grep, based on the file names, 
#e.g.  cat scaleExps.csv | grep "control "