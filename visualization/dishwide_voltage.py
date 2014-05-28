#!/usr/bin/python

import os.path
import argparse
from matplotlib import pyplot as plt
import sys
sys.path.append("../common")
import labviewloader


#For a dish, generate a histogram of the voltages in 0.00001 volt wide bins
#across each channel, over all samples

#Plot multiple data in multiple images
def plotMultiImage(data):
    channelNum = 0;
    for channel in data:
        plt.figure(figsize=(25,6))
        plt.plot(channel)
        plt.savefig(baseTableName + "_v_ch_{0}.png".format(channelNum))
        channelNum += 1
        plt.clf()

#Plot all data together in the same image
def plotSingleImage(data):
    axisNum = 0
    plt.figure(figsize=(20,12))
    skip = 0
    for row in range(8):
        for col in range(8):
            axisNum += 1
            
            
            #skip the corners
            if (row == 0) and (col == 0):
                skip += 1
                continue
            if (row == 0) and (col == 7):
                skip += 1
                continue 
            if (row == 7) and (col == 0):
                skip += 1
                continue 
            if (row == 7) and (col == 7):
                skip += 1
                continue 
           
            ax = plt.subplot(8, 8, axisNum)
            
            channel = (axisNum - skip) -1
            #samples = ll.getDataCol(channel)
            samples = data[channel]
            plt.plot(samples)
            plt.ylim(-0.009, 0.009)
            ax.set_yticklabels([])
            ax.set_xticklabels([])
    plt.tight_layout()
    plt.savefig(baseTableName + ".png")


if __name__ == '__main__':
    # Get the input file name
    argparser = argparse.ArgumentParser("Load and graph a labview LVM file")
    argparser.add_argument("file_path", type=str, nargs=1, help="The file to load.")
    argparser.add_argument('-m', dest="multi_image", action='store_false')
    args = argparser.parse_args()
    infileName = args.file_path[0]
    
    #Create a figure name for storing the data
    baseTableName = os.path.basename(infileName).split('.')[-2]
    extent = os.path.basename(infileName).split('.')[-1]
    baseTableName = baseTableName.replace(" ", "_")
    
    data = []
    if extent == "csv":
        #load into 2D array
        data = []
        for channels in range(60):
            data.append([])
        with open(infileName, "r") as inputFile:
            #Get a line and convert it to floating point numbers
            for line in inputFile:
                values = [float(val) for val in line.split(',')]
                #Load into the data array
                for index in range(60):
                    data[index].append(values[index])
                
                    
    else: #This had better be an LVM file
        # Load the data file
        ll = labviewloader.LabViewLoader()
        ll.load(infileName)
    
        #Convert to a list of lists (2D array). Each list is a channel, 60 channels. 
        for channelNum in range(60):
            samples = ll.getDataCol(channelNum)
            samples = [float(str(sample)) for sample in samples] 
            data.append(samples)
            
    if args.multi_image:
        plotMultiImage(data)
    else:
        plotSingleImage(data)
                