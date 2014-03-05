#!/usr/bin/python

import sys
sys.path.append("../common")
import labviewloader
import plotdish
from scipy import signal, fftpack
import numpy
import pygame

#May be very slow, as this doesn't use FFTs for speedup
def correlate(sigA, sigB):
    return numpy.correlate(sigA, sigB)

#Circular correlation, should be faster for big signals
#From http://stackoverflow.com/questions/4688715/find-time-shift-between-two-similar-waveforms
#This returns the shift for which the sum of the signals is maximized. 
def circCorrelate(sigA, sigB):
    A = fftpack.fft(sigA)
    B = fftpack.fft(sigB)
    Ar = -A.conjugate()
    Br = -B.conjugate()
    return numpy.argmax(numpy.abs(fftpack.ifft(Ar*B)))

def colorMap (maxVal, minVal, value):
    maxColor = 255.0
    minColor = 0.0
    value = float(value)
    maxVal = float(maxVal)
    minVal = float(minVal)
    color = int((x - minVal) * (maxColor - minColor) / (maxVal - minVal) + minColor)
    #This is a gray with a value depending on where value falls between max and min val
    return (color, color, color)

def renderAll(allPairs):
    #Find the largest and smallest values
    maxCorr = 0
    minCorr = 0
    for xx in xrange(60):
        for yy in xrange(60):
            maxCorr = max(maxCorr, max(allPairs[(xx,yy)]))
            minCorr = min(minCorr, min(allPairs[(xx,yy)]))

    size = width,height = 600,600
    screen = pygame.display.set_mode(size)
    screen.fill((0,255,0))
    
    for tt in xrange(len(allPairs[(0,0)])):            
        for xx in xrange(60):
            for yy in xrange(60):
                corr = allPairs[(xx,yy)][tt]
                color = colorMap(maxCorr, minCorr, corr)
                pygame.draw.rect(screen, color, pygame.Rect(xx*10, yy*10, 10, 10))
        pygame.display.flip()
        pygame.image.save(screen, "test_frame_{0}.png".format(tt))
                
if __name__ == '__main__':
    #Start pygame for later drawing
    pygame.init()
    
    #Get a labview lvm file off the command line and load it
    infile = sys.argv[1]
    ll = labviewloader.LabViewLoader()
    ll.load(infile)
    
    #How many samples to drop from the data
    drop = 400
    
    for iiA in xrange(60): #For each channel
        dataA = ll.getDataCol(iiA)[drop:]
        allCorr = []
        for iiB in xrange(60): #For each other chanel
            correlations = []
            dataB = ll.getDataCol(iiB)[drop:]
            for tt in xrange(100):
                #Plot correlation of dataB to dataA for the first 100 shifts
                correlations.append(correlate(dataA, dataB)[0])
                item = dataB.pop(0)
                dataB.append(item)
            allCorr.append(correlations)
        #Plot all the correlations between the point and all others    
        plotdish.plotdish(allCorr, "{0}-all-correlations".format(iiA))
        
    
            
        
