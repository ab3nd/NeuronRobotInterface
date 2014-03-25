#!/usr/bin/python
from pickle import Unpickler
import ConfigParser
import sys
import argparse
sys.path.append("../common")
import PhysicalDish

#Loads a neuron location file and a neuron type file, to be able to indicate 
#which neurons are located around a specific point in a culture

def buildPadNeuronMap(config, physDish):
    #Get some configuration parameters to set which neurons are connected to which 
    #of the receiving pads of the MEA
    pad_rows = config.getint("mea", "pad_rows")
    pad_cols = config.getint("mea", "pad_cols")
    pad_dia = config.getint("mea", "pad_diameter")
    pad_spacing = config.getint("mea", "pad_spacing")
    sensing_range = config.getint("mea", "sensing_range")
        
    #For each pad, get a list of nearby neurons and their distance from the pad
    pad_neuron_map = {}
    for pad_x in xrange(0,pad_rows):
        for pad_y in xrange (0,pad_cols):
            #Had some ignore-corners code here, but we can't ignore the corners, because those are our
            #ground reference points
            
            #Get the location of the pad  
            pad_location = physDish.getPadLocation(pad_x, pad_y)
            
            #Get the neurons within the sensing range of the pad
            sensed_neurons = physDish.getNeighbors(pad_location, sensing_range)
            
            ranged_neurons = []
            for neuron in sensed_neurons:
                neuron_location = physDish.getLocation(neuron)
                distance = physDish.euclidDist(pad_location, neuron_location)
                ranged_neurons.append((neuron, distance))
                
            #Add the list of close neurons to the current pad
            pad_neuron_map[(pad_x, pad_y)] = ranged_neurons  

    return pad_neuron_map

if __name__ == '__main__':
    #Initialize the connections and neuron locations from files
    argp = argparse.ArgumentParser(description='Run a culture simulation based on connection and layout files')
    argp.add_argument('-l', dest='loc_path')
    argp.add_argument('-t', dest='type_path')
    args = argp.parse_args()
    
    #Get the location file name
    locFile = args.loc_path
    locations = None
    with open(locFile) as inFile:
        locations = Unpickler(inFile).load()
    
    #Get the neuron type file name
    typeFile = args.type_path
    types = None
    with open(typeFile) as inFile:
        types = Unpickler(inFile).load()
    
    configFile = "../plating_simulator/basic_sim.cfg"
    
    #Load the configuration from the config file
    config = ConfigParser.ConfigParser()
    config.readfp(open(configFile))
    
    #Load a physical representation of the dish
    physDish = PhysicalDish.PhysicalLayout(config)
    physDish.loadMaps(locations)
    
    #Build a pad to neuron map
    padsToNeurons = buildPadNeuronMap(config, physDish)
    
    for key in sorted(padsToNeurons.keys()):
        totalInhib = 0;
        totalExcite = 0;
        for neuron in padsToNeurons[key]:
            #if neuron[0] in types
            if neuron[0] in types["inhib"]:
                #totalInhib += 1
                #include distance, more distant neurons contribute less
                totalInhib += 1.0/((neuron[1] + 1) ** 2)
            else:
                #totalExcite += 1
                totalExcite += 1.0/((neuron[1] + 1) ** 2)
        print "{0}\t{1}\t{2}\t{3}\t{4}".format(key, round(totalInhib,3), round(totalExcite,3), round((float(totalInhib)/float(totalExcite)),3), round(totalInhib - totalExcite, 3))
        