#!/usr/bin/python
import sys
sys.path.append("../common")
import labviewloader
import argparse
import numpy as np
from decimal import Decimal
import matplotlib.pyplot as plt
import csv
import os

# Convert a set of samples into Brian-esque spike timing data
def chn2spike(data, channel, deltaT):
	asFloats = [float(str(sample)) for sample in data]
	mean = np.average(asFloats)
	stdDev = np.std(asFloats)
	# Zero-mean the data to make the spike detection easier
	zeroMean = [sample - mean for sample in asFloats]
	thresh = stdDev * 3

   # Brian format is pairs (i, t) where i is a neuron number and t is
   # the time at which it fired.
	spikes = []
	for ii in range(0, len(asFloats)):
		#Positive and negative spikes
		if (asFloats[ii] > thresh) or (asFloats[ii] < -thresh):
			spikes.append((channel, deltaT * ii))
            # Note that this has decimal precision problems with the time
	return spikes

if __name__ == '__main__':
    # Get the input file name
    argparser = argparse.ArgumentParser("Load and graph a labview LVM file")
    argparser.add_argument("file_path", type=str, nargs=1, help="The file to load.")
    args = argparser.parse_args()
    
    allspikes = []
    
    # Handle CSV files too
    if args.file_path[0].endswith(".csv"):
    	channels = 60
     	samples = 30000
    	data = [[] * channels]
    	# Assemble the columns, each column is one channel
    	with open(args.file_path[0]) as infile:
    		reader = csv.read(infile, delimiter=",", quoting=csv.QUOTE_NONE)
    		for row in reader:
    			for ii in range(0, channels):
    				data[ii].append(row[ii])
    	# Process into spikes
    	for channel in range(0, channels):
    		chData = data[channel]
    		spikes = chn2spike(data, channel, deltaT)
    		allspikes.extend(spikes)
    else:
    	# Load the file
    	ll = labviewloader.LabViewLoader()
    	ll.load(args.file_path[0])
    
    	# for each channel, calculate the spike timings
    	channels = int(ll.getHeaderValue("Channels", 1))
    	samples = int(ll.getHeaderValue("Samples", 1))
    	# Time step between each sample
    	deltaT = float(ll.getHeaderValue("Delta_X", 1))
    
       # collect all the spike data
    	for channel in range(0, channels):
    		data = ll.getDataCol(channel)
    		spikes = chn2spike(data, channel, deltaT)
    		allspikes.extend(spikes)

    #Create a filename to save it as
    basename = os.path.basename(args.file_path[0]).split(".")[0]
    imageName = basename + "-spikes.png"
    
    #Plot the data
    channels, times = zip(*allspikes)
    fig = plt.gcf()
    defaultSize = fig.get_size_inches()
    fig.set_size_inches(200,7.5)
    plt.scatter(times, channels)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Recording site")
    plt.savefig(imageName)

