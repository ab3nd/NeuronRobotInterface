#!/usr/bin/python

import sys
import os
import rosbag
import subprocess
import yaml
import roslib
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

# Given a ros bag file, flip through all the images in it and output the X,Y position of the 
# center of the largest collection of red pixels in the image

def getRedObject(image, timestamp):
    image = np.asarray(image)
    
    #Convert to HSV
    HSVimage = cv2.cvtColor(image, cv2.cv.CV_BGR2HSV)
    #Split into H, S, and V planes
    H, S, V = cv2.split(HSVimage)
    
    #Threshold the image to only keep red pixels
    retval, Hthresh = cv2.threshold(H, 165, 65536, cv2.THRESH_BINARY)
    #Threshold to remove undersaturated red
    retval, Sthresh = cv2.threshold(S, 45, 65536, cv2.THRESH_BINARY)
    redPx = cv2.bitwise_and(Hthresh, Sthresh)
    
    #Dilate all the pixels
    kernel = np.ones((3,3), 'uint8')
    redPx = cv2.erode(redPx, kernel)
    kernel = np.ones((11,11), 'uint8')
    redPx = cv2.dilate(redPx, kernel)
    #image = redPx
    #Find contours 
    #First, find edges using canny edge detection
    #edges = cv2.Canny(redPx, 200, 400)
    #contours, heirarchy = cv2.findContours(edges, cv2.cv.CV_RETR_EXTERNAL, cv2.cv.CV_CHAIN_APPROX_SIMPLE)
    #contours, heirarchy = cv2.findContours(edges, cv2.cv.CV_RETR_LIST, cv2.cv.CV_CHAIN_APPROX_NONE)
    contours, heirarchy = cv2.findContours(redPx, cv2.cv.CV_RETR_EXTERNAL, cv2.cv.CV_CHAIN_APPROX_SIMPLE)
    
    #Get the largest contour
    areas = [cv2.contourArea(c) for c in contours]
    maxIdx = np.argmax(areas)
    bigContour = contours[maxIdx]
    
    #Draw its bounding box
    x,y,w,h = cv2.boundingRect(bigContour)
    #cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0))
    
    #Draw its center
    center = (x+w/2, y+w/2)
    #radius = 5
    #cv2.circle(image, center, radius, (255,255,0))
    
    #Draw the other contours too
    #cv2.drawContours(image, contours, -1, (255,0,0))
    #cv2.imwrite("frame_{0}.png".format(timestamp), image)
    return center
    
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
    
    #Create a cv bridge to convert the image
    bridge = CvBridge()
      
    #Read the messages
    bag = rosbag.Bag(bagfile)
    totalMotion = 0 #Start at zero
    startTime = None
    with open(outfileroot + "_cup.csv", 'w') as outfile:
        outfile.write("StartTime,Motion\n")
        for topic, msg, t in bag.read_messages(topics=['/gscam/image_raw']):
            if startTime is None:
                startTime = t
            try:
                cvImage = bridge.imgmsg_to_cv(msg, "bgr8")
            except CvBridgeError, e:
                print e
            timestamp = str((t-startTime).to_sec())
            location = getRedObject(cvImage, timestamp)
#             motions = msg.move.states
#             totalMotion += motions[1] #The Y axis, left or right on the arm
            outfile.write(timestamp + "," + str(location[0]) + "," + str(location[1]) + "\n")
            
    