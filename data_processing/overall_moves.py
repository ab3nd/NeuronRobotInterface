#!/usr/bin/python

import cv2
import sys
import os
import rosbag
import subprocess
import yaml
import cv_bridge
import numpy as np
#Checks all the motions made by the arm over the course of a run
#Outputs stats on runs

def imgToMove(msg):
    #Convert it to an OpenCV image
    bridge = cv_bridge.CvBridge()
    cvImg = np.array(bridge.imgmsg_to_cv(msg, "bgr8"), dtype=np.uint8)
    #Threshold it, parameters from ImageSlicer.cpp
    hsvImg = cv2.cvtColor(cvImg, cv2.cv.CV_BGR2HSV)
    H,S,V = cv2.split(hsvImg)
    H = cv2.threshold(H, 165, 65536, cv2.cv.CV_THRESH_BINARY)
    S = cv2.threshold(S, 45, 65536, cv2.cv.CV_THRESH_BINARY)
    out = cv2.bitwise_and(H[1], S[1])

    #Slice it and count white pixels
    slices = 5
    counts = []
    regionWidth = out.shape[1]/slices
    for ii in range(slices):
        roi = out[0:out.shape[0],ii*regionWidth:(ii*regionWidth)+regionWidth]
        counts.append(cv2.countNonZero(roi))
        
    #Decide on a move
    bestMove = "N"
    leftCount = rightCount = 0
    for ii in range(3):
        leftCount += counts[ii]
        rightCount += counts[4-ii]
    if abs(leftCount - rightCount) > 500:
        #Enough difference, we move
        if leftCount > rightCount:
            bestMove = "L"
        else:
            bestMove = "R"
    else:
        #Not different enough, no move
        bestMove = "N"
    return bestMove

def armCmdToMove(msg):
    motions = msg.move.states
    #Left is 1, right is -1. Oddly, the arm regards L/R as the Y axis
    if motions[1] > 0:
        return "L"
    elif motions[1] < 0:
        return "R"
    else:
        #This probably doesn't happen with constant move commands,
        #because "No move" is just letting the current command time out,
        #rather than sending a command to stop. 
        return "N"

if __name__ == "__main__":
    #Parse the command line argument 
    if len(sys.argv) < 2:
        print "Please specify the bag file to read"
        sys.exit(1)      
    bagfile = sys.argv[1]
    
    #Come up with an output file root name
    outfileroot = "./" + os.path.basename(bagfile).split('.')[0]
    
    #Load the yaml output of calling rosbag info on the input file. 
    fileInfo = yaml.load(subprocess.Popen(['rosbag', 'info', '--yaml', bagfile], stdout=subprocess.PIPE).communicate()[0])
      
    #Read the messages
    bag = rosbag.Bag(bagfile)
    totalMotion = 0 #Start at zero
    startTime = None
    with open(outfileroot + "_overall.csv", 'w') as outfile:
        for topic, msg, t in bag.read_messages(topics=['/constant_move_times']):
            if startTime is None:
                startTime = t
            motions = msg.move.states
            totalMotion += motions[1] #The Y axis, left or right on the arm
            outfile.write(str(totalMotion) + "," + str((t-startTime).to_sec())+"\n")
            
    