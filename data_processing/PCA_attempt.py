#!/usr/bin/python

import sys
sys.path.append("../../common")
import labviewloader
import numpy as np
from matplotlib import pyplot as plt
import pprint
import os

def sliceList(inList, length, step):
    outList = []
    index = 0
    #Don't work in reverse, don't run forever
    if step <= 0:
        step = 1
    while index < len(inList)-length:
        outList.append(inList[index:index+length])
        index += step
    #outList.append(inList[index:])
    return outList

def main(fileName):
    #Create a big array of all the data
    window_size = 100
    window_shift = 100
        
    # Load the data file
    ll = labviewloader.LabViewLoader()
    ll.load(fileName)
    
    #Get the first channel
    data = ll.getDataCol(0)
    data = [float(item) for item in data]
    
    #Break it into a list of lists, and that into a numpy array
    input_data = np.array(sliceList(data, window_size, window_shift))
    
    #Calculate the sample mean vector and the std dev vector
    sample_mean = np.mean(input_data, axis=0)
    sample_std_dev = np.std(input_data, axis=0)
    
    #Subtract the sample mean from the data and divide by the std dev. 
    zero_mean = []
    for row in input_data:
        zero_mean.append((row - sample_mean)/sample_std_dev)
    zero_mean = np.array(zero_mean)
    
    #Compute the covariance matrix
    coVar = np.cov(zero_mean)
    
    #Do the SVD
    U, s, V = np.linalg.svd(coVar, full_matrices=True)
    #U, s, V = np.linalg.svd(input_data, full_matrices=True)
    plt.scatter(U[0:,0], U[0:,1])
    '''
    for label, x, y in zip(labels, U[:,0], U[:,1]):
        plt.annotate(
            label, 
            xy = (x, y), xytext = (-3, 3),
            textcoords = 'offset points', ha = 'right', va = 'bottom')
    '''
    outfile  = "./PCA_" + os.path.basename(fileName).split(".")[0] + ".png"
    plt.savefig(outfile)

if __name__ == '__main__':
    main(sys.argv[1])
