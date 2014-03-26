#!/usr/bin/python

import sys
sys.path.append("../common")
import labviewloader
import plotdish
import numpy
import pygame
import os
                
if __name__ == '__main__':
    
    #Get a labview lvm file off the command line and load it
    infile = sys.argv[1]
    ll = labviewloader.LabViewLoader()
    ll.load(infile)

    #Create a filename to save the output to
    basename = os.path.basename(infile).split(".")[0]
    imageName = basename + "-voltages"
    
    #Collect all the data for each channel
    allData = []    
    for ii in xrange(60):
        data = ll.getDataCol(ii)
        #allData.append(data)
        allData.append(data[250:])
        
    #Plot all the voltages
    plotdish.plotdish(allData, imageName)

