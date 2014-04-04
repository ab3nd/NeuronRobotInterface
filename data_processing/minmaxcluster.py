#!/usr/bin/python

#Segment an LVM file and attempt to cluster the segments
import numpy as np
from matplotlib import pyplot as plt
import pprint
import os
import pickle
import sys
sys.path.append("../../common")
import labviewloader
    
def sliceList(inList, length, step, deltaT):
    outList = []
    index = 0
    #Don't work in reverse, don't run forever
    if step <= 0:
        step = 1
    while index < len(inList)-length:
        start = index * deltaT
        timeLen = length * deltaT
        outList.append((np.array(inList[index:index+length]), start, timeLen))
        index += step
    #Don't bother with leftover data at end
    #outList.append(inList[index:])
    return outList

def euclidDistance(p1, p2):
    if len(p1) != len(p2):
        print "Points are not of the same dimensionality"
        sys.exit()
    #For the moment, naive Euclidian distance 
    return np.linalg.norm(p1-p2)

def computeDistance(p1, p2):
    #return euclidDistance(p1, p2)
    return doTheTimeWarp(p1, p2)


#Slightly more efficient, only one list comprehension
def zeroMeanUnitNorm(data):
    if len(data):
        mean = sum(data) / len(data)
        maxVal = max(data)
        return np.array([(x-mean)/maxVal for x in data])
    else:
        return data  
#TODO TRY WINDOWED TIMEWARP

#TODO label the sections
    
#Find the cost of dynamic time-warping alignment between two vectors
def doTheTimeWarp(v1, v2):
    #Empty table of time-warp costs
    DTW = np.zeros((len(v1), len(v2)))
    #Set up the table
    for i in range(1, len(v1)):
        DTW[i][0] = np.inf
    for i in range(1, len(v2)):
        DTW[0][i] = np.inf
    DTW[0][0] = 0
    
    for i in range(1, len(v1)):
        for j in range(1, len(v2)):
            cost=abs(v1[i]-v2[j])
            DTW[i][j] = cost + min([DTW[i-1][j], DTW[i][j-1], DTW[i-1][j-1]])
    #print DTW.shape
    return DTW[len(v1)-1, len(v2)-1]
               
# After T.F. Gonzalez, Clustering to Minimize the Maximum Intercluster Distance, 
# Theoretical Computer Science 38, p293, Oct 1983
def maxmincluster(data, k):
    #Normalize each bit independently
    #data = [zeroMeanUnitNorm(item) for item in data]
    #Do the clustering
    heads = [data[0]]
    clusters = [data]
    for l in range(k):
        maxDist = 0     #Store the maximum distance found so far
        maxCindex = 0   #Store the index of the cluster it was in
        maxDindex = 0   #Store the index of the item in the cluster
        #For all the clusters
        for cIndex in range(len(clusters)):
            #Find the node farthest from the head of its cluster
            for dIndex in range(len(clusters[cIndex])):
                distance = computeDistance(heads[cIndex][0], clusters[cIndex][dIndex][0])
                if distance > maxDist:
                    maxDist = distance
                    maxCindex = cIndex
                    maxDindex = dIndex
        #Got a new cluster head
        newHead = clusters[maxCindex][maxDindex]
        newCluster = []
        #For all the existing clusters
        for cIndex in range(len(clusters)):
            #Split the current cluster into items that it keeps and 
            #items that it loses to the new cluster
            keep = [a for a in clusters[cIndex] if computeDistance(heads[cIndex][0], a[0]) < computeDistance(newHead[0], a[0])]
            move = [a for a in clusters[cIndex] if computeDistance(heads[cIndex][0], a[0]) >= computeDistance(newHead[0], a[0])]
            clusters[cIndex] = keep
            newCluster.extend(move)
        heads.append(newHead)
        clusters.append(newCluster)
        
        #Debugging
        for ii in range(len(heads)):
            print "Head {0}: cluster size:{1}".format(ii, len(clusters[ii]))
        print "\n"
        
    #Compose into a list of tuples, the first item is the head, the second is its cluster
    fullClustering = zip(heads, clusters)
    return fullClustering
        
def main(fileName, window_size, window_shift):
    #Create a big array of all the data
    #100/20 was pretty good
    #window_size = 10
    #window_shift = 5
    print "Processing {0} with window size {1} and shift {2}".format(fileName, window_size, window_shift)
    input_data = []
        
    #Work with labview files
    if fileName.endswith(".lvm"):    
        # Load the data file
        ll = labviewloader.LabViewLoader()
        ll.load(fileName)
        
        #Get the first channel
        data = ll.getDataCol(0)
        data = [float(item) for item in data]
        
        #Get the timestep between samples
        deltaT = float(ll.getHeaderValue("Delta_X",0))
        
        #Break it into a list of lists, and that into a numpy array
        input_data = sliceList(data, window_size, window_shift, deltaT)
    #Work with averaged lvm files
    elif fileName.endswith(".avg"):
        data = []
        with open(fileName, "r") as infile:
            for line in infile:
                data.append(float(line))
        deltaT = 0.001
        input_data = sliceList(data, window_size, window_shift, deltaT)
    else:
        print "This script only works on LVM files and averaged data (.avg files)"
        sys.exit()
          
    #Adapt cluster count based on data set size
    clusterCount = len(input_data)/50
    #Cluster the data 
    clusters = maxmincluster(input_data, clusterCount)
    
    #Scribble it out to a file
    with open("minmax{0}_{1}.p".format(window_size, window_shift), "w") as outfile:
        pickle.dump(clusters, outfile)
    
    index = 0
    data_to_id = {}
    for cluster in clusters:
        exemplar = cluster[0]
        members = cluster[1]
        
        #Plot the exemplar, then plot the members under it
        plt.figure(figsize=(20,25))
        #The head gets a separate plot
        plt.subplot(2,1,1)
        plt.plot(exemplar[0])
        #The members get plotted together
        plt.subplot(2,1,2)
        for member in members:
            plt.plot(member[0])
            
            #Turn the cluster data inside-out to make a lookup table for 
            #converting each item of input data into its respective cluster
            #identifier. This only uses the start and end times because
            #the data is in an unhashable data type. 
            data_to_id[(member[1],member[2])] = index

        #Write to a file
        plt.savefig("cluster_{0}.png".format(index))
        plt.close()
        index += 1
    
    #Use the data and the lookup table to build 
    #a list of of cluster IDs that represents the data
    with open("clusterList.csv", "w") as outfile:
        for sampleSet in input_data:
            outfile.write(str(data_to_id[(sampleSet[1],sampleSet[2])]) + "\n")
    
if __name__ == '__main__':
    #File, window, step
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
