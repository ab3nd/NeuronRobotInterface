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
        outfile.write("StartTime,Motion\n")
        for topic, msg, t in bag.read_messages(topics=['/constant_move_times']):
            if startTime is None:
                startTime = t
            motions = msg.move.states
            totalMotion += motions[1] #The Y axis, left or right on the arm
            outfile.write(str((t-startTime).to_sec()) + "," + str(totalMotion) + "\n")
            
    