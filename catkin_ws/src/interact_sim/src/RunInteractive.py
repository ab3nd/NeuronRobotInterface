#!/usr/bin/python

'''
Run a given connectivity interactively, reading a camera image and 
outputting a dish state as if this were zanni or a real dish. 
''' 

from pickle import Unpickler
from brian import *
import ConfigParser
from brian.library.IF import *
import random
sys.path.append("../../../../common")
import PhysicalDish
import StimData
import re
import argparse
import os

#Ros libs for getting images
import roslib; roslib.load_manifest('img_slicer')
import rospy
from img_slicer.srv import *

#Stimulation scheduler as used by the non-interactive version. 
#Stimulations are scheduled, and then delivered as the running MEA advances from state to state.             
class stimScheduler:
    
    def __init__(self, config):
        #Get the runtime in seconds
        self.timeLen = config.getfloat("runtime", "run_len") * second
        self.sampleRate = config.getfloat("runtime", "stim_sample_rate")
        self.sampleLen = int(self.timeLen*self.sampleRate)
        self.schedules = {}
        self.updateMethod = None
        self.sampleIndex = 0;
    
    #Add a stimulation consisting of the values in data, applied to channel channel, starting at offset seconds  
    #Offset should be in floating point seconds into the runtime. 
    def add(self, data, channel, offset):
        #Create an empty stimulation channel 
        if not channel in self.schedules.keys():
            self.schedules[channel] = [0] * self.sampleLen 
        
        #Calculate the offset in samples
        sOffset = int(offset * self.sampleRate)
        
        #Trim data to fit
        overage = (len(data) + sOffset) - len(self.schedules[channel])
        if overage > 0: 
            data = data[0:len(data) - overage]
        
        #Copy the data into the schedule at the proper offset
        self.schedules[channel][sOffset:sOffset+len(data)] = data[:]    
    
    def nextStimState(self):
        #Generate a list of (channel, voltage) pairs
        currentStates = []
        for channel in self.schedules.keys():
            currentStates.append((channel, self.schedules[channel][self.sampleIndex]))
        self.sampleIndex += 1
        #Don't run off the end of the schedule
        if self.sampleIndex > self.sampleLen:
            self.sampleIndex = self.sampleLen
        return currentStates


class dynamicScheduler(stimScheduler):
    
    def __init__(self):
        #Map of channels to their index in the stimulation waveform
        self.channelIndicies = {}
        #List of channels that are currently stimulating
        self.stimulatingChannels = []

    def start(self, channel):
        #Don't start if already stimulating on that channel
        if channel not in self.stimulatingChannels:
            self.stimulatingChannels.append(channel)
            self.channelIndicies[channel] = 0
        
    def nextStimState(self):
        stoppedChannels = []
        currentStates = []
        for channel in self.stimulatingChannels:
            #Increment the index
            self.channelIndicies[channel] += 1
            if self.channelIndicies[channel] >= len(StimData.training_signal):
                #If we're done stimulating, add it to the removal list
                stoppedChannels.append(channel)
            else:
                #Otherwise, get the next voltage and add it to the current states
                currentStates.append((channel, StimData.training_signal[self.channelIndicies[channel]]))
        
        for channel in stoppedChannels:
            if channel in self.stimulatingChannels:
                self.stimulatingChannels.remove(channel)       
        return currentStates

class imageHandler:
    def __init__(self):
        print("Waiting for image service to come online")
        rospy.wait_for_service('red_px_counts')
        print("Image service online")
        self.counts = []
        self.leftCount = 0
        self.rightCount = 0
        self.isLeft = self.isRight = self.isCenter = False
         
    def update(self):
        try:
            getRedPx = rospy.ServiceProxy('red_px_counts', ImageSlicer)
            self.counts = getRedPx(5)
        except rospy.ServiceException, e:
            print "Service call failed in RunInteractive: %s"%e
        for ii in range(3):
            self.leftCount += self.counts.pixelCount[ii]
            self.rightCount += self.counts.pixelCount[4-ii]
        if abs(self.leftCount - self.rightCount) < 500:
            self.isLeft = False
            self.isRight = False
            self.isCenter = True
        else:
            if self.leftCount > self.rightCount:
                self.isLeft = True
                self.isRight = False
                self.isCenter = False
            else:
                self.isLeft = False
                self.isRight = True
                self.isCenter = False
            
    def cupIsLeft(self):
        return self.isLeft
        
    def cupIsRight(self):
        return self.isRight
    
    def cupIsCenter(self):
        return self.isCenter
    
    def cupIsVisible(self):
        #See if there's a column with a lot of red in it
        for column in self.counts.pixelCount:
            if column > 800:
                return True
        return False
                    
class meaRunner:
    
    def __init__(self, tFile, cFile, lFile, config):
        #As was loaded from file
        self.config = config
        
        #Load the connections and locations of the neurons
        #Connections are stored as a list of (a,b) tuples, which indicate that 
        #the neuron with ID a synapses onto the neuron with ID b. 
        with open(cFile) as inFile:
            self.connections = Unpickler(inFile).load()
        
        #Locations are stored as an array of possible neuron locations. Each element of 
        #the array contains either -1 (no neuron) or a neuron ID number
        with open(lFile) as inFile:
            self.locations = Unpickler(inFile).load()
        
        #Neuron types are stored in a hash with two keys. 
        #  "inhib" - a list of inhibitory neuron IDs
        #  "excite" - a list of excitatory neuron IDs
        with open(tFile) as inFile:
            self.neuron_types = Unpickler(inFile).load()
            
        #Set the date based on the location file
        self.file_date = re.search("_([\-:0-9]*)\.", lFile).group(1)
        days = self.file_date.split("-")
        self.file_date_short = "{0}/{1}/{2}".format(days[0], days[1], days[2])
        mins = days[3].split(":")
        self.file_time = "{0}:{1}:{2}.{3}".format(mins[0], mins[1], mins[2], 0.0)
        
        #Build a physical representation of the dish
        self.physDish = PhysicalDish.PhysicalLayout(self.config)
        self.physDish.loadMaps(self.locations)
        
        #Get the largest neuron id, which is also the number of neurons - 1 
        self.neuronCount = 0
        for row in reversed(self.locations):
            self.neuronCount = max(row)
            if max(row) > 0:
                break
        self.neuronCount += 1
        
        #The Brian model, with the connectivity and neuron models used
        self.culture = None
      
        #The which pads are near which neurons
        self.pad_neuron_map = None
        
        #Stimulus schedule, if this remains None, no stim will be delivered
        self.stimSchedule = None

        #Use an image handler to update dynamic stim scheduler. 
        #TODO this is bad OO design, but expedient
        self.imgHandler = None
        
        #self.plateSender = None
        
    def setStimSchedule(self, stimSched):
        self.stimSchedule = stimSched
    
    def setImageHandler(self, hndlr):
        self.imgHandler = hndlr
    
    #def setPlateSender(self, sender):
    #    self.plateSender = sender
        
    def runSim(self):
        
        if self.pad_neuron_map is None:
            self.buildPadNeuronMap()

        #Set up neuron population and initial voltage
        self.neuron_count = int(self.physDish.getCellCount())

        #Load which neurons are excitatory and which are inhibitory from the 
        #neuron type pickle file (generated by SeedMea.py)
        inhib_neurons = self.neuron_types["inhib"]
        inhib_count = len(inhib_neurons)
        excite_neurons = self.neuron_types["excite"]
        
        #This is for intrinsic bursting (IB) neurons.
        #The parameters are set based on values from Izhikevich, "Simple Model of Spiking Neurons"
        #a and b are a and b from the paper, for the reset, Vr is c (the reset voltage) and 
        #b is d (after-spike reset of recovery variable) in the paper. 
        ibModel = Izhikevich(a=0.02/ms, b=0.2/ms) 
        #Vr and b are (I think) c and d from the same paper
        ibReset = AdaptiveReset(Vr=-65*mvolt, b=2*nA)
         
        #Regular spiking neurons (RS)
        rsModel = Izhikevich(a=0.02/ms, b=0.2/ms) 
        rsReset = AdaptiveReset(Vr=-65*mvolt, b=8*nA)
         
        #Chattering neurons (CH)  
        ibModel = Izhikevich(a=0.02/ms, b=0.2/ms) 
        ibReset = AdaptiveReset(Vr=-50*mvolt, b=2*nA)   
         
        #Fast spiking (FS)
        fsModel = Izhikevich(a=0.1/ms, b=0.2/ms)
        fsReset = AdaptiveReset(Vr=-65*mvolt, b=2*nA)
         
        #Low-threshold spiking (LTS)
        fsModel = Izhikevich(a=0.02/ms, b=0.25/ms)
        fsReset = AdaptiveReset(Vr=-65*mvolt, b=2*nA)
                 
        #TODO the two groups are likely redundant, but won't be if the 
        #inhibitory and excitatory neurons become different subgroups, with different
        #activity models
        self.culture = NeuronGroup(self.neuron_count, rsModel, threshold=30*mV, reset=rsReset)
        Pe = self.culture.subgroup(self.neuron_count-inhib_count)
        Pi = self.culture.subgroup(inhib_count)
        Pi.model=fsModel
        Pi.reset=fsReset
         
        #Connections between the two groups
        C = Connection (self.culture, self.culture)
        for connection in self.connections:
            if connection[0] in inhib_neurons:
                #From Izhikevich, Simple Model of Spiking Neurons, the inhibitory connections should be
                #around -1*(excitatory_weight/2)
                C[connection[0], connection[1]] = -5*mV
            else:
                C[connection[0], connection[1]] = 10*mV
 
        #Izhikevich neurons require stimulation or nothing happens
        #Reduced to 10mV to see if it affects the standard deviation
        pI = PoissonInput(Pi, N=1, rate = 0.5*Hz, weight=1*mV, state='vm')
        pE = PoissonInput(Pe, N=1, rate = 0.5*Hz, weight=0.5*mV, state='vm')
        
        #Monitor the voltages of the neurons that are within the recording distance of pads
        toRecord = []
        for pad in self.pad_neuron_map.keys():
            toRecord.extend([entry[0] for entry in self.pad_neuron_map[pad]])
            
        #Strip dupes. This loses order.
        toRecord = list(set(toRecord))
        
        # Create a monitor to record the voltages of each neuron every 1 ms.
        # If timestep = 1, then 10 actions are recorded every ms.
        # If timestep = 10, then 1 action is recorded every ms.
        # Setting timestep to 1 is in effect 30 s of simulation in just 3 s.
        vMonitor = StateMonitor(self.culture, "vm", record=toRecord, timestep=10)
        
        M = SpikeMonitor(self.culture)
        
        
        #Start up the stimulation scheduler
        if self.stimSchedule is not None:
            #Set up a cache for which neurons are near stimulated pads
            stimNeurons = {}
            
            #Set up a network_operation to get updates from the stim scheduler
            #Stimulation data was recorded at 1k-sample/second
            stimClock=Clock(dt=1*ms)
            @network_operation(stimClock)
            def updateStim():
                chVoltages = self.stimSchedule.nextStimState()
                for channel, voltage in chVoltages:
                    if channel not in stimNeurons.keys(): 
                        #Get the neurons near that pad
                        x,y = self.physDish.channelToPad(channel)
                        x,y = self.physDish.getPadLocation(x, y)
                        stimNeurons[channel] = self.physDish.getNeighbors((x,y), self.config.getint("mea", "sensing_range"))
                #Add voltage based on their distance from the pad
                for channel, voltage in chVoltages:
                    neuronIDs = stimNeurons[channel]
                    for nID in neuronIDs:
                        #Get the distance
                        x, y = self.physDish.channelToPad(channel)
                        dist = self.physDish.euclidDist(self.physDish.getLocation(nID), self.physDish.getPadLocation(x,y))
                        #Inverse square law, if the distance is zero, this is just the voltage
                        vNeuron = voltage * (float(1.0)/((dist**2) +1.0))
                        #Apply the voltage
                        self.culture[nID].vm += vNeuron

            #If we have an image handler to coordinate with the stimulator
            #Note that these times are sim time, not real time                        
            if self.imgHandler is not None:
                imgUpdateClock=Clock(dt=1*ms)
                @network_operation(imgUpdateClock)
                def updateImage():
                    self.imgHandler.update()
                    if self.imgHandler.cupIsVisible():
                         if self.imgHandler.cupIsLeft():
                             self.stimSchedule.start(47)
                         elif self.imgHandler.cupIsRight():
                             self.stimSchedule.start(54)
                 
        #Do the actual run
        #TODO: This can't be separated into a different function without Brian failing
        print "running simulation...",
        #Set this up to have the voltages read out by the server
        readClock=Clock(dt=1*ms)
        server = RemoteControlServer(clock=readClock)
        run(self.config.getfloat("runtime", "run_len") * second)
        self.writeLabview(vMonitor)
        
    def buildPadNeuronMap(self):
        print "Building pad -> neuron map..."
        #Get some configuration parameters to set which neurons are connected to which 
        #of the receiving pads of the MEA
        pad_rows = self.config.getint("mea", "pad_rows")
        pad_cols = self.config.getint("mea", "pad_cols")
        pad_dia = self.config.getint("mea", "pad_diameter")
        pad_spacing = self.config.getint("mea", "pad_spacing")
        sensing_range = self.config.getint("mea", "sensing_range")
        ignore_corners = True #Corner electrodes are frequently used as reference points, not recorded
            
        #For each pad, get a list of nearby neurons and their distance from the pad
        self.pad_neuron_map = {}
        for pad_x in xrange(0,pad_rows):
            for pad_y in xrange (0,pad_cols):
                #Had some ignore-corners code here, but we can't ignore the corners, because those are our
                #ground reference pointse
                
                #Get the location of the pad  
                pad_location = self.physDish.getPadLocation(pad_x, pad_y)
                
                #Get the neurons within the sensing range of the pad
                sensed_neurons = self.physDish.getNeighbors(pad_location, sensing_range)
                
                ranged_neurons = []
                for neuron in sensed_neurons:
                    neuron_location = self.physDish.getLocation(neuron)
                    distance = self.physDish.euclidDist(pad_location, neuron_location)
                    ranged_neurons.append((neuron, distance))
                    
                #Add the list of close neurons to the current pad
                self.pad_neuron_map[(pad_x, pad_y)] = ranged_neurons   
        print "Done."
        
    def writeLabview(self, vMonitor):
        pad_rows = self.config.getint("mea", "pad_rows")
        pad_cols = self.config.getint("mea", "pad_cols")

        fname = "./labview_{0}.lvm".format(self.file_date)
        count = 1
        #Find a file name that's not taken
        while os.path.isfile(fname):
            fname = "./labview_{0}_{1}.lvm".format(self.file_date, count)
            count += 1
        
        # Write a log file in the labview format
        with open(fname, "w") as outfile:
            outfile.write(
'''LabVIEW Measurement\t
Writer_Version\t2
Reader_Version\t2
Separator\tTab
Decimal_Separator\t.
Multi_Headings\tYes
X_Columns\tOne
Time_Pref\tAbsolute
Operator\tSimulation Data
Date\t{0}
Time\t{1}
***End_of_Header***\t
\t
'''.format(self.file_date_short, self.file_time))
            outfile.write(                                                                                                                                                                                                                              
'''Channels\t60
Samples\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}
Date\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}
Time\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}
Y_Unit_Label\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts
X_Dimension\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime
X0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0
Delta_X\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100\t0.00100
***End_of_Header***\t
X_Value\tVoltage_0 (Filtered)\tVoltage_1 (Filtered)\tVoltage_2 (Filtered)\tVoltage_3 (Filtered)\tVoltage_4 (Filtered)\tVoltage_5 (Filtered)\tVoltage_6 (Filtered)\tVoltage_7 (Filtered)\tVoltage_8 (Filtered)\tVoltage_9 (Filtered)\tVoltage_10 (Filtered)\tVoltage_11 (Filtered)\tVoltage_12 (Filtered)\tVoltage_13 (Filtered)\tVoltage_14 (Filtered)\tVoltage_15 (Filtered)\tVoltage_16 (Filtered)\tVoltage_17 (Filtered)\tVoltage_18 (Filtered)\tVoltage_19 (Filtered)\tVoltage_20 (Filtered)\tVoltage_21 (Filtered)\tVoltage_22 (Filtered)\tVoltage_23 (Filtered)\tVoltage_24 (Filtered)\tVoltage_25 (Filtered)\tVoltage_26 (Filtered)\tVoltage_27 (Filtered)\tVoltage_28 (Filtered)\tVoltage_29 (Filtered)\tVoltage_30 (Filtered)\tVoltage_31 (Filtered)\tVoltage_32 (Filtered)\tVoltage_33 (Filtered)\tVoltage_34 (Filtered)\tVoltage_35 (Filtered)\tVoltage_36 (Filtered)\tVoltage_37 (Filtered)\tVoltage_38 (Filtered)\tVoltage_39 (Filtered)\tVoltage_40 (Filtered)\tVoltage_41 (Filtered)\tVoltage_42 (Filtered)\tVoltage_43 (Filtered)\tVoltage_44 (Filtered)\tVoltage_45 (Filtered)\tVoltage_46 (Filtered)\tVoltage_47 (Filtered)\tVoltage_48 (Filtered)\tVoltage_49 (Filtered)\tVoltage_50 (Filtered)\tVoltage_51 (Filtered)\tVoltage_52 (Filtered)\tVoltage_53 (Filtered)\tVoltage_54 (Filtered)\tVoltage_55 (Filtered)\tVoltage_56 (Filtered)\tVoltage_57 (Filtered)\tVoltage_58 (Filtered)\tVoltage_59 (Filtered)\tComment
'''.format(self.file_date_short, self.file_time, len(vMonitor.times)))
            
            #The data, represented as a 2-D array, X is sample sites, Y is time
            all_data = np.zeros(((pad_rows*pad_cols) + 1, len(vMonitor.times)))
            
            #The channel means, for normalization
            channelMeans = np.zeros(pad_rows*pad_cols + 1)

            #The voltage is measured relative to a bath electrode, so the potentials are measured
            #from (effectively) a point on the outside of the cell and point in the dish far from all
            #cells, which I think this does an okay job of approximating. 
            for index in range(0, len(vMonitor.times)): 
                all_data[0, index] = index
                for pad in self.pad_neuron_map.keys(): 
                    #import pdb; pdb.set_trace()
                    neurons = self.pad_neuron_map[pad]
                    total = 0.0
                    for neuron in neurons:
                        #Sum of the neuron voltages multiplied by the inverse square of the 
                        #distance from the pad to the neuron. 
                        try:
                            total += 1/((neuron[1] + 1) **2) * vMonitor[neuron[0]][index]
                        except:
                            import pdb; pdb.set_trace()
                    #The pads don't come out in a particular order, this reorders them
                    all_data[(pad[0] + pad[1]*pad_rows) + 1, index] = total
                    channelMeans[(pad[0] + pad[1]*pad_rows) + 1] += total
            
            #Make them actual means, rather than just sums
            channelMeans = [x/len(vMonitor.times) for x in channelMeans]
            
            #Subtract the means from each channel in order to center everything at zero
            for row in range(0, len(vMonitor.times)):
                all_data[:,row] = all_data[:,row] - channelMeans
                
                #Then print the value, after pulling out the corner pads
                entry = all_data[:,row]
                entry = np.delete(entry, [(pad_cols * pad_rows), ((pad_cols * (pad_rows-1)) + 1), pad_rows, 1])

                #Print the time
                outfile.write(str(float(entry[0])/1000))
                entry = np.delete(entry, 0)
                
                #Write the rest of the values to the file
                for value in entry:
                    outfile.write('\t')
                    outfile.write(str(value)) # - vGround))    
                outfile.write('\n')  
                
            outfile.close()
            print "done."  

def main():
    #Initialize the connections and neuron locations from files
    argp = argparse.ArgumentParser(description='Run a culture simulation based on connection and layout files')
    argp.add_argument('-c', dest='conn_path')
    argp.add_argument('-l', dest='loc_path')
    argp.add_argument('-t', dest='type_path')
    args = argp.parse_args()
    
    #Get the connection file name
    connFile = args.conn_path
    #Get the location file name
    locFile = args.loc_path
    #Get the neuron type file name
    typeFile = args.type_path 
     
    configFile = "./basic_sim.cfg"
    
    #Load the configuration from the config file
    config = ConfigParser.ConfigParser()
    config.readfp(open(configFile))
    
    #intialize an imageHandler    
    imgHandler = imageHandler()
    
    #initalize a dynamic stimulator
    stim = dynamicScheduler()
        
    #pSender = plateStateSender()
    
    #Create the runner and add the stims
    mr = meaRunner(typeFile, connFile, locFile, config)
    mr.setStimSchedule(stim)
    mr.setImageHandler(imgHandler)
    #mr.setPlateSender(pSender)
    mr.runSim()
    
    

if __name__ == '__main__':
    main()