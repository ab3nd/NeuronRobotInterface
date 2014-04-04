#!/usr/bin/python
import sys
import numpy as np
import pickle

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

def centroid(cluster):
    #Put the head of the cluster in as the centroid
    center = cluster[0][0]
    count = 1
    #Now add all the members
    members = cluster[1]
    for member in members:
        center = np.add(center, member[0])
        count += 1
    center = np.divide(center, count)
    return center
        
def avgDist(center, cluster):
    members = cluster[1]
    distance = 0
    for member in members:
        distance += doTheTimeWarp(member[0], center)
    return distance/float(len(members))

#Calculate the Davies-Bouldin Index over clusters 
def daviesBouldin(clusters):
    n = len(clusters)
    total = 0
    for cluster1 in clusters:
        c1Centroid = centroid(cluster1)
        c1AvgDist = avgDist(c1Centroid, cluster1)
        maxSubIndex = 0
        for cluster2 in clusters:
            if (cluster1[0][0] == cluster2[0][0]).all():
                #These have the same head, and so are the same cluster
                continue
            c2Centroid = centroid(cluster2)
            c2AvgDist = avgDist(c2Centroid, cluster2)
            canidate = ((c1AvgDist + c2AvgDist)/doTheTimeWarp(c1Centroid, c2Centroid))
            if canidate > maxSubIndex:
                maxSubIndex = canidate
        total += maxSubIndex
    total = total/n
    print "Davies-Bouldin Index: {0} (low is good)".format(total)
    return total

def intraClusterDistance(cluster):
    distance = 0
    for item1 in cluster:
        for item2 in cluster:
            if (item1[0]==item2[0]).all():
                continue
            canidate = doTheTimeWarp(item1, item2)
            if canidate > distance:
                distance = canidate
    return distance

def allDistances(cluster):
    center = centroid(cluster)
    centerDists = []
    allPointsDists = []
    
    if len(cluster[1]) == 1:
        #There is only one member in this cluster
        centerDists = [0.0]
        allPointsDists = [0.0]
    else:    
        #Calculate all the distances
        for item1 in cluster[1]:
            d1 = item1[0]
            #Distance to the center of the cluster
            centerDists.append(doTheTimeWarp(center, d1))
            #Distance to all other points
            for item2 in cluster[1]:
                d2 = item2[0]
                if (d1 == d2).all():
                    continue
                allPointsDists.append(doTheTimeWarp(d1, d2))

    return [centerDists, allPointsDists]

#Calculate the Dunn Index over clusters
def dunnIndex(clusters):
    #Precompute the maximum intra-cluster distance
    maxIntraD = 0
    dunnIdx = float("inf")
    for cluster in clusters:
        iD = intraClusterDistance(cluster[1])
        if iD > maxIntraD:
            maxIntraD = iD
            
    for cluster1 in clusters:
        center1 = centroid(cluster1)
        for cluster2 in clusters:
            if (cluster1[0][0] == cluster2[0][0]).all():
                #These have the same head, and so are the same cluster
                continue
            center2 = centroid(cluster2)
            canidate = doTheTimeWarp(center1, center2)/maxIntraD
            if canidate < dunnIdx:
                dunnIdx = canidate
    print "Dunn Index: {0} (high is good)".format(dunnIdx)
    return dunnIdx

#From http://www.physics.rutgers.edu/~masud/computing/WPark_recipes_in_python.html
def meanstdv(x): 
    from math import sqrt 
    n, mean, std = len(x), 0, 0 
    for a in x: 
        mean = mean + a 
    mean = mean / float(n) 
    for a in x: 
        std = std + (a - mean)**2 
        std = sqrt(std / float(n-1)) 
    return mean, std

def tightness(clusters):
    for cluster in clusters:
        ev
        if len(cluster[1]) > 1:            
            distances = allDistances(cluster)
            #unpack the values
            centerDists = distances[0]
            allDists = distances[1]
            mean, stdDev = meanstdv(centerDists)
            #Center distances
            outline = "{0},{1},{2},{3},".format(max(centerDists), min(centerDists), mean, stdDev)
            mean, stdDev = meanstdv(allDists)
            outline += "{0},{1},{2},{3}".format(max(allDists), min(allDists), mean, stdDev)
            print outline
        else:
            print "Cluster only has one member"
            
def main(fileName):
    #Unpickle the data. 
    #The clusters are stored as a list of 2-tuples
    #The first item is the head subwindow of the cluster, the second 
    #item is a list of subwindows in the cluster. Each subwindow is a 3-tuple
    #of a numpy array of the data, the start time of the data, and the 
    #length of the data in time
    clusterData = pickle.load(open(fileName, "rb"))
   
    tightness(clusterData) 
    #daviesBouldin(clusterData)
    #dunnIndex(clusterData) 

if __name__ == '__main__':
    main(sys.argv[1])