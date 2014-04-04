#!/usr/bin/python
import sys
sys.path.append("../common")
import labviewloader 
from decimal import Decimal

def zeroMean(data):
    mean = Decimal(0.0)
    if len(data):
        mean = Decimal( sum(data)) / len(data)
    else:
        return data
    #Subtract mean to shift data down
    return [x - mean for x in data] 

def unitNorm(data):
    if len(data):
        maxVal = max(data)
        return [x/maxVal for x in data]
    else:
        return data
    
#Slightly more efficient, only one list comprehension
def zeroMeanUnitNorm(data):
    if len(data):
        mean = Decimal(sum(data)) / len(data)
        maxVal = max(data)
        return [(x-mean)/maxVal for x in data]
    else:
        return data  
    
if __name__ == '__main__':    
    
    channel = 5
    infile_path = "../data_sets/labview/lvm_files/Stimulation Experiment/13March/13Mar-singlestim 1.lvm"
    
    ll = labviewloader.LabViewLoader()
    ll.load(infile_path)
    
    # Load the channel
    channel_data = ll.getDataCol(channel)
    
    print channel_data[0:10]
    #These end up the same
    print zeroMean(unitNorm(channel_data))[0:10]
    print zeroMeanUnitNorm(channel_data)[0:10]
    #Slightly different, I suspect rounding error
    print unitNorm(zeroMean(channel_data))[0:10]
    
    #These tests passed
    #print channel_data[0:10]
    #Normalize to unit norm
    #print unitNorm(channel_data)[0:10]
    #Doing it twice shouldn't change anything (max becomes 1 on the first pass)
    #print unitNorm(unitNorm(channel_data))[0:10]
    
    #These tests passed
    #print channel_data[0:10]
    #Perform the zero-mean operation
    #print zeroMean(channel_data)[0:10]
    #Doing it twice shouldn't change anything
    #print zeroMean(zeroMean(channel_data))[0:10]