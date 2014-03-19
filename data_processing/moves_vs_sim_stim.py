#!/usr/bin/python

import sys
import os
import rosbag
import subprocess
import yaml

# Output the arm movement in a form that can easily be graphed. 

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

def checkMotion(mTime, motion):
    #This describes the motion commands for 
    
    # 2.5 seconds off
    if mTime < 2.5:
        return 0
    
    # 5 seconds left
    if mTime > 2.5 and mTime < 7.5 and motion > 0:
        return 1 
    else:
        return 0
    
    # 2.5 seconds off
    if mTime > 7.5 and mTime < 10:
        return 0

    # 5 seconds right
    if mTime > 10 and mTime < 15 and motion < 0:
        return 1 
    else:
        return 0

    # 2.5 seconds off
    if mTime > 15 and mTime < 17.5:
        return 0

    # 5 seconds left
    if mTime > 17.5 and mTime < 22.5 and motion > 0:
        return 1 
    else:
        return 0

    # 2.5 seconds off
    if mTime > 22.5 and mTime < 25:
        return 0

    # 5 seconds right
    if mTime > 2.5 and mTime < 7.5 and motion < 0:
        return 1 
    else:
        return 0
        
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
            outfile.write(str((t-startTime).to_sec()) + "," + str(totalMotion) + "," + str(checkMotion((t-startTime).to_sec(), motions[1])) + "\n")