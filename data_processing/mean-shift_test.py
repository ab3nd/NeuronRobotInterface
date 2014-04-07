#!/usr/bin/python

#Attempt to cluster sub-sampled snippets of a signal using mean-shift clustering from scikit

from sklearn.cluster import MeanShift, estimate_bandwidth, DBSCAN
import sys
import numpy as np
import matplotlib.pyplot as plt
import colorsys
import random
import re
from pprint import pprint
from matplotlib import cm
import pdb
#import stuff that I wrote
import sliceTest as sl
sys.path.append("../common")
import labviewloader
import zero_mean_unit_norm as zmun

def renderClusters(labels_unique, labels, input_data):
    #render ten of some label
    for lNum in labels_unique:
        count = 10
        fig = plt.figure()
        for label, sample in zip(labels, input_data):
            if label == lNum:
                plt.plot(sample)
                count -= 1
            if count < 0:
                break
        fig.savefig("first10-{0}.png".format(lNum))
        plt.close()

#From http://stackoverflow.com/a/9701141
def get_colors(num_colors):
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return colors

#Create a unique color for each unique item in the list
def genColors(list):
    uniques = np.unique(list)
    colorCode = {}
    colors = get_colors(len(uniques))
    return dict(zip(uniques, colors))

def renderFullSignal(data, deltaT, labels, input_data, window_size, window_shift, ignore_list=[0], name="full.png"):
    fig = plt.figure()
    #Render the image huge
    fig.set_size_inches(300,25)
    plt.plot(data)
    
    #Generate a set of unique colors for each label
    colors = genColors(labels)
    
    #for color in colors.keys():
    #    print color, colors[color]
    
    #Flip through all the labels    
    #The length of each box drawn is the length of the sample
    for index in range(len(labels)):
        label = labels[index]
        #Label 0 should be ignored, it is the "no other cluster" cluster
        if label not in ignore_list:
            color = colors[label]
            #Draw a box. X coords are in data units, y coords are in the range 0-1
            #X start of the box is the size of the sample offset times the index of the sample
            xmin = index * window_shift
            #X end of the box is the start of the box plus the sample length
            xmax = xmin + window_size
            plt.axvspan(xmin, xmax, ymin=0.25, ymax=0.75, alpha=0.4, ec="none", fc=colors[label])
     
     
    fig.savefig(name)
    plt.close()

def indexToShift(window_size, window_shift, deltaT):
    return lambda x: window_shift * x * deltaT

if __name__ == '__main__':
    
    #Get a labview lvm file off the command line and load it
    infile = sys.argv[1]
    ll = labviewloader.LabViewLoader()
    ll.load(infile)
    
    #Get the window size and shift between windows
    window_size = int(sys.argv[2])
    window_shift = int(sys.argv[3])
    
    #Get a channel, zero mean and unit norm it, and convert to floats
    channel = int(sys.argv[4])
#     channel = random.randrange(60)
    data = ll.getDataCol(channel)
    data = zmun.zeroMeanUnitNorm(data)
    data = [float(item) for item in data]
    
    #Get the timestep between samples
    deltaT = float(ll.getHeaderValue("Delta_X",0))
    
    #Break it into a list of lists, and that into a numpy array
#     window_size = 20
#     window_shift = 6
    #import pdb; pdb.set_trace()
    input_data = sl.sliceList(data, window_size, window_shift)
    #sliceList includes any leftovers as the last item, so ditch that
    input_data.pop()
    
    #Convert to a numpy array-like to give to scikit
    dataArray = np.asarray(input_data)
    
    
    #Try mean-shift clustering. I want something a little looser (so lower bandwidth, oddly) 
    #than the usual estimates, but not by a lot. 
    #bandwidth = estimate_bandwidth(dataArray, quantile=0.01, n_samples = 1000)
    #For some reason, previous version got *** ValueError: zero-size array to maximum.reduce without identity
    bandwidth = estimate_bandwidth(dataArray, quantile=0.01)
    print "Estimated bandwidth {0}".format(bandwidth)
    
    #Try mean-shift clustering
    msCluster = MeanShift(bandwidth=bandwidth)# cluster_all = False)
    msCluster.fit(dataArray)
    labels = msCluster.labels_
    
    #Try DBSCAN
    #for dist in np.arange(0.1,10.0,0.01):
    #db = DBSCAN(eps=6.08, min_samples=1).fit(dataArray)
    #labels = db.labels_
    labels_unique = np.unique(labels)
    n_clusters = len(labels_unique)
    print "Estimated {0} clusters over {1} items with eps={2}".format(n_clusters, len(labels), 6.08)

    #Get the count of each label
    labelCounts = {}
    for l in sorted(labels_unique):
        lCount = len([y for y in labels if y == l])
        labelCounts[l] = lCount
    
    counts = [(label, labelCounts[label]) for label in labels_unique]
    counts.sort(key=lambda x: x[1])
    for item in counts:
        print item[0],",", item[1]
         
 
    renderClusters(labels_unique, labels, input_data)
    #renderFullSignal(data, deltaT, labels, input_data, window_size, window_shift)
    
       
    #Convert the channel into a string of labels separated by commas
    strLabels = [str(x) for x in labels]
    asLabels = ','.join(strLabels)
    #Strip out multiple instances of the zero channel
    asLabels = re.sub("(,0)+", ",0", asLabels)
    #This is where you would save it as CSV data, if that's what you want 
    asLabels = [int(x) for x in asLabels.split(",")]
    
    followCounts = {}
    maxCount = 0
    for index, item in enumerate(asLabels):
        #Don't run off the end of the list
        if index == len(asLabels)-3:
            break

        #Skip zero cluster (misc/noise)
        if item == 0:
            continue
        
        #Find the next item, skipping misc/noise entries
        next = -1
        try:
            if asLabels[index+1] == 0:
                next = asLabels[index+2]
            else:
                next = asLabels[index+1]
        except:
            import pdb; pdb.set_trace()
            
        #new value
        if item not in followCounts.keys():
            followCounts[item] = {}
            followCounts[item][next] = 1
    
        #value we have seen before, new next item
        else:
            if next not in followCounts[item].keys():
                followCounts[item][next] = 1
            else:
                followCounts[item][next] += 1

        #Store the maximum follow count for graphing
        if followCounts[item][next] < maxCount:
            maxCount = followCounts[item][next]
            
    #pprint(followCounts)
    
    #Generate a table of correlations, according to the relationships 
    followArray = np.zeros((n_clusters, n_clusters))
    for xx in range(1, n_clusters):
        for yy in range(1, n_clusters):
            flw = followCounts[xx]
            if yy in flw.keys():
                followArray[xx,yy] = flw[yy]
    
    #pprint(followArray)
    # Make plot with vertical (default) colorbar
    fig, ax = plt.subplots()
    
    cax = ax.imshow(followArray, interpolation='nearest', cmap=cm.coolwarm)
    ax.set_title('Follow counts')
    
    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    cbar = fig.colorbar(cax, ticks = [x for x in range(0,maxCount)])
    cbar.ax.set_yticklabels([str(x) for x in range(0, maxCount)])
    
    #plt.show()
    fig.savefig("relation_ch_{0}.png".format(channel))
     
    #Get the most common follower and the region it comes after
#     max = 0
#     maxFirst = 0
#     maxFollows = 0
#     for first in followArray.keys():
#         follows = followArray[first]
#         for second in follows.keys():
#             if follows[second] < max:
#                 maxFirst = first
#                 maxFollows = second
#                 max = follows[second]
#                 print maxFirst, maxFollows, max

    #import pdb; pdb.set_trace()
    pairwiseList = []            
    for first in followCounts.keys():
        for second in followCounts[first].keys():
            pairwiseList.append((first, second, followArray[first][second]))
    
          
    pairwiseList = sorted(pairwiseList, key=lambda x:x[2])
    pairwiseList.reverse()
    
    for item in pairwiseList:
        #Don't care about rare cases
        if item[2] < 2:
            break
        print "For cluster {0}, which occurs {1} times:".format(item[0], labelCounts[item[0]])
        if item[1] not in followCounts.keys():
            #Get just the pair of rows out of labels
            ignore = list(set(labels) - set([item[0], item[1]]))
            renderFullSignal(data, deltaT, labels, input_data, window_size, window_shift, ignore_list = ignore, name="marked-{0}-{1}.png".format(item[0], item[1]))
            print "   {0} comes after {1} {2} times, but {1} never comes after {0}".format(item[0], item[1], item[2])            
        else:
            if item[0] not in followCounts[item[1]].keys():
                #Get just the pair of rows out of labels
                ignore = list(set(labels) - set([item[0], item[1]]))
                renderFullSignal(data, deltaT, labels, input_data, window_size, window_shift, ignore_list = ignore, name="marked-{0}-{1}.png".format(item[0], item[1]))                
                print "   {0} comes after {1} {2} times, but {1} never comes after {0}".format(item[0], item[1], item[2])            
            else:
                print "   {0} comes after {1} {2} times, but {1} comes after {0} {3} times".format(item[0], item[1], item[2], followCounts[item[1]][item[0]])        
        print ""
    
