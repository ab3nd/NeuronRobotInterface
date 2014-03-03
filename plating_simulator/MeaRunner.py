#!/usr/bin/python
'''
Classes to run a MEA network, based on the connectivity generated by SeedMea. 

By subclassing, the neuron model, logging method, and so forth can be modified. 

''' 

from pickle import Unpickler
from brian import *
import ConfigParser
from brian.library.IF import *
import random
import PhysicalDish
import StimData
import re
import argparse


            
class stimScheduler:
    
    def __init__(self, config):
        #Get the runtime in seconds
        self.timeLen = config.getfloat("runtime", "run_len") * second
        self.sampleRate = config.getfloat("runtime", "stim_sample_rate")
        self.sampleLen = int(self.timeLen/self.sampleRate)
        self.schedules = {}
        self.updateMethod = None
    
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
        
class meaRunner:
    
    def __init__(self, cFile, lFile, config):
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
        
        #Set the date based on the location file
        import pdb; pdb.set_trace
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
    
    def setStimSchedule(self, stimSched):
        self.stimSchedule = stimSched
            
    def runSim(self):
        
        if self.pad_neuron_map is None:
            self.buildPadNeuronMap()
            
        eqs = '''
        dv/dt = (ge+gi-(v+49*mV))/(20*ms) : volt
        dge/dt = -ge/(5*ms) : volt
        dgi/dt = -gi/(10*ms) : volt
        '''
        self.culture = NeuronGroup(self.neuronCount , eqs, threshold=-50*mV, reset=-60*mV)
        self.culture.v = -60 * mV + 10 * mV * rand(len(self.culture))

        #Partition population between inhibitory and excitatory
        inhib_count = int(self.neuronCount * self.config.getfloat("population","inhibitory_rate")/100)
        excitory_count = self.neuronCount - inhib_count 
        #Pe = self.culture.subgroup(excitory_count)
        #Pi = self.culture.subgroup(inhib_count)
        
        #TODO: THIS SHOULD HAVE BEEN SAVED WHEN GENERATING THE NETWORK AND LOADED, NOT DONE HERE
        #Set up connections. First, pick a random set of inhibitory neuron ids. 
        #Everything else is excitatory. Then create the connection objects and 
        #populate them according to the connectivity list
        inhib_neurons = random.sample(xrange(self.neuronCount), inhib_count)
        excite_neurons = list(set(xrange(self.neuronCount)) - set(inhib_neurons))
        
        #Connections between the two groups
        Ce = Connection(self.culture, self.culture, 'ge')#, weight=1.62*mV, sparseness=0.02)
        Ci = Connection(self.culture, self.culture, 'gi')
        debugDecimate = 10
        for connection in self.connections:
            #prune = random.randint(0,100)
            #if prune < debugDecimate:
                if connection[0] in inhib_neurons:
                    Ci[connection[0], connection[1]] = -9*mV 
                else:
                    Ce[connection[0], connection[1]] = 1.62*mV

        
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
        vMonitor = StateMonitor(self.culture, "v", record=toRecord, timestep=10)
        
        M = SpikeMonitor(self.culture)
        
        #Start up the stimulation scheduler
        if self.stimSchedule is not None:
            self.stimSchedule.begin()
        
        #Do the actual run
        #TODO: This can't be separated into a different function without Brian failing
        print "running simulation...",
        run(self.config.getfloat("runtime", "run_len") * second)
        self.writeLabview(vMonitor)
        
    def buildPadNeuronMap(self):
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

    def writeLabview(self, vMonitor):
        pad_rows = self.config.getint("mea", "pad_rows")
        pad_cols = self.config.getint("mea", "pad_cols")

        # Write a log file in the labview format
        with open("./labview_{0}.lvm".format(self.file_date), "w") as outfile:
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
                    neurons = self.pad_neuron_map[pad]
                    total = 0.0
                    for neuron in neurons:
                        #Sum of the neuron voltages multiplied by the inverse square of the 
                        #distance from the pad to the neuron. 
                        total += 1/((neuron[1] + 1) **2) * vMonitor[neuron[0]][index]
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
    args = argp.parse_args()
    
    #Get the connection file name
    connFile = args.conn_path
    #Get the location file name
    locFile = args.loc_path
     
    configFile = "./basic_sim.cfg"
    
    #Load the configuration from the config file
    config = ConfigParser.ConfigParser()
    config.readfp(open(configFile))
    
    #Create a stim scheduler
    ss = stimScheduler(config)
    #Schedule a stimulation
    ss.add(StimData.training_signal, 3, 1)
    
    #Create the runner and add the stims
    mr = meaRunner(connFile, locFile, config)
    mr.setStimSchedule(ss)
    mr.runSim()
    
    

if __name__ == '__main__':
    main()