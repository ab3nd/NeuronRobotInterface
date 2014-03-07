#!/usr/bin/python
import rosbag
import sys
import os
import time
import subprocess
import yaml
import pprint

def buildHeader(sampleCount):
    t = time.localtime()
    #Build a date string of the format Month/Day/Year
    dateStr = time.strftime("%m/%d/%Y", t)
    #Build a time string of the format Hours:Minutes:Seconds.fractions
    timeStr = time.strftime("%H:%M:%S.00",t)
    return '''LabVIEW Measurement\t
Writer_Version\t2
Reader_Version\t2
Separator\tTab
Decimal_Separator\t.
Multi_Headings\tYes
X_Columns\tOne
Time_Pref\tAbsolute
Operator\tBagfile Dump
Date\t{0}
Time\t{1}
***End_of_Header***\t
\t
Channels\t60
Samples\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}
Date\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}
Time\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}
Y_Unit_Label\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts
X_Dimension\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime
X0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0
Delta_X\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100
***End_of_Header***\t
X_Value\tVoltage_0 (Filtered)\tVoltage_1 (Filtered)\tVoltage_2 (Filtered)\tVoltage_3 (Filtered)\tVoltage_4 (Filtered)\tVoltage_5 (Filtered)\tVoltage_6 (Filtered)\tVoltage_7 (Filtered)\tVoltage_8 (Filtered)\tVoltage_9 (Filtered)\tVoltage_10 (Filtered)\tVoltage_11 (Filtered)\tVoltage_12 (Filtered)\tVoltage_13 (Filtered)\tVoltage_14 (Filtered)\tVoltage_15 (Filtered)\tVoltage_16 (Filtered)\tVoltage_17 (Filtered)\tVoltage_18 (Filtered)\tVoltage_19 (Filtered)\tVoltage_20 (Filtered)\tVoltage_21 (Filtered)\tVoltage_22 (Filtered)\tVoltage_23 (Filtered)\tVoltage_24 (Filtered)\tVoltage_25 (Filtered)\tVoltage_26 (Filtered)\tVoltage_27 (Filtered)\tVoltage_28 (Filtered)\tVoltage_29 (Filtered)\tVoltage_30 (Filtered)\tVoltage_31 (Filtered)\tVoltage_32 (Filtered)\tVoltage_33 (Filtered)\tVoltage_34 (Filtered)\tVoltage_35 (Filtered)\tVoltage_36 (Filtered)\tVoltage_37 (Filtered)\tVoltage_38 (Filtered)\tVoltage_39 (Filtered)\tVoltage_40 (Filtered)\tVoltage_41 (Filtered)\tVoltage_42 (Filtered)\tVoltage_43 (Filtered)\tVoltage_44 (Filtered)\tVoltage_45 (Filtered)\tVoltage_46 (Filtered)\tVoltage_47 (Filtered)\tVoltage_48 (Filtered)\tVoltage_49 (Filtered)\tVoltage_50 (Filtered)\tVoltage_51 (Filtered)\tVoltage_52 (Filtered)\tVoltage_53 (Filtered)\tVoltage_54 (Filtered)\tVoltage_55 (Filtered)\tVoltage_56 (Filtered)\tVoltage_57 (Filtered)\tVoltage_58 (Filtered)\tVoltage_59 (Filtered)\tComment
'''.format(dateStr, timeStr, sampleCount)

#Parse the command line argument 
if len(sys.argv) < 2:
    print "Please specify the file to read"
    sys.exit(1)
    
bagfile = sys.argv[1]
outfileName = "./" + os.path.basename(bagfile).split('.')[0] + ".lvm"

#Load the bag file
bag = rosbag.Bag(bagfile)

#initialize some parameters
deltaT = 0.001 #Fake timestamps
currentT = 0.0
lines = []

#Load the yaml output of calling rosbag info on the input file. 
fileInfo = yaml.load(subprocess.Popen(['rosbag', 'info', '--yaml', bagfile], stdout=subprocess.PIPE).communicate()[0])

#Get the total count of messages out
zanniInfo = [t for t in fileInfo['topics'] if t['topic'] == '/zanni']
samples = zanniInfo[0]['messages']

with open(outfileName, 'w') as outfile:
    outfile.write(buildHeader(samples))
    #Build an array of the lines of the file
    for topic, msg, t in bag.read_messages(topics=['/zanni']):
        #Compose a line of a fake timestamp, the data, and a newline
        fileLine = str(currentT) + '\t' + '\t'.join([str(x) for x in msg.voltages]) + "\n"
        currentT += deltaT
        outfile.write(fileLine)
                
bag.close()