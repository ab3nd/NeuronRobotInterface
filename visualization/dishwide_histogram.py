#!/usr/bin/python

import os.path
import argparse
from matplotlib import pyplot as plt
import sys
sys.path.append("../../common")
import labviewloader


#For a dish, generate a histogram of the voltages in 0.00001 volt wide bins
#across each channel, over all samples

if __name__ == '__main__':
    # Get the input file name
    argparser = argparse.ArgumentParser("Load and graph a labview LVM file")
    argparser.add_argument("file_path", type=str, nargs=1, help="The file to load.")
    argparser.add_argument('-m', dest="multi_image", action='store_false')
    args = argparser.parse_args()
    infileName = args.file_path[0]
    
    #Create a figure name for storing the data
    baseTableName = os.path.basename(infileName).split('.')[-2]
    baseTableName = baseTableName.replace(" ", "_")
    
    # Load the data file
    ll = labviewloader.LabViewLoader()
    ll.load(infileName)

    if args.multi_image:
        axisNum = 0
        channelNum = 0
        plt.figure(figsize=(20,12))
        for row in range(8):
            for col in range(8):
                axisNum += 1
                
                 
                #skip the corners
                if (row == 0) and (col == 0):
                    continue
                if (row == 0) and (col == 7):
                    continue 
                if (row == 7) and (col == 0):
                    continue 
                if (row == 7) and (col == 7):
                    continue 
                ax = plt.subplot(8, 8, axisNum)
                #Get the channel
                samples = ll.getDataCol(channelNum)
                channelNum += 1
                #Convert from Decimal, lose precision, so sad
                samples = [float(str(sample)) for sample in samples]
                
                maxSample = max(samples)
                minSample = min(samples)
                binCount = 1000
                n, bins, patches = plt.hist(samples, binCount)
                ax.set_yticklabels([])
                ax.set_xticklabels([])
    
        plt.tight_layout()
        plt.savefig(baseTableName + ".png")
    else:
        for channelNum in range(60):
            samples = ll.getDataCol(channelNum)
            samples = [float(str(sample)) for sample in samples]
            n, bins, patches = plt.hist(samples, binCount)
            plt.savefig(baseTableName + "_ch_{0}.png".format(channelNum))
            plt.clf()
        