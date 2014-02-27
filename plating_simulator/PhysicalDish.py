# Class which stores the physical layout of the MEA, with the location of the pads
# and location of the individual neurons. This does not deal with connectivity,
# or the electrical model of the neurons. 
import math
import numpy as np
import Image
import random


    
class PhysicalLayout:
    def __init__(self, config):
        #Set up the physical constraints of the environment
        self.soma_dia = config.getfloat("neuron", "soma_diameter")
        
        # Get the diameter of the (circular) MEA retaining ring 
        dish_width = config.getfloat("mea", "mea_diameter") 
        # Convert to a square with equivalent area
        self.dish_width = int(math.sqrt(math.pi * (dish_width/2)**2))
        
        #Maximum dendrite length
        dendrite_max = config.getfloat("neuron", "dendrite_max_len")
        #Distance of maximum connections
        axon_growth = config.getfloat("neuron", "axon_max_len")
        #Axons cannot reach out of dish
        axon_max = dish_width
        soma_dia = config.getfloat("neuron", "soma_diameter")
        
        # Get the diameter of the (circular) MEA retaining ring 
        dish_width = config.getfloat("mea", "mea_diameter") 
        # Convert to a square with equivalent area
        dish_width = int(math.sqrt(math.pi * (dish_width/2)**2))
        #Assume neurons are square, don't pile up
        self.cells_per_edge = int(dish_width/soma_dia)
        
        #This is where the bounds checking would be if I were super-clever

        #Calculate the locations of the MEA pads 
        #For each pad, calculate the location of the pad in grid coordinates
        pad_rows = config.getint("mea", "pad_rows")
        pad_cols = config.getint("mea", "pad_cols")
        pad_dia = config.getint("mea", "pad_diameter")
        self.pad_spacing = config.getint("mea", "pad_spacing")
    
        #In order to figure out where a pad is in the culture, some conversion needs to be done
        #Get the values in uM
        pad_array_width = ((pad_cols-1) * self.pad_spacing) + pad_dia
        pad_array_height = ((pad_rows-1) * self.pad_spacing) + pad_dia
        #Assumes dish is square and pad is centered in it
        self.pad_top = (dish_width - pad_array_width)/2
        self.pad_left = (dish_width - pad_array_height)/2
                
    #Given a pad grid location, convert it to a culture grid location. 
    #The pads are usually an 8x8 grid, numbered like this:
    #    0 1 2 3 4 5 6 7  So (0,0) is on the top left
    #  0 * * * * * * * *  
    #  1 * * * * * * * * 
    #  2 * * * * * * * * 
    #  3 * * * * * * * * 
    #  4 * * * * * * * * 
    #  5 * * * * * * * * 
    #  6 * * * * * * * * 
    #  7 * * * * * * * * 
    def getPadLocation(self, x, y):
        pad_x = self.pad_left + (x * self.pad_spacing)
        pad_y = self.pad_top + (y * self.pad_spacing)
        #Convert to grid coordinates
        return (int(pad_x/self.soma_dia), int(pad_y/self.soma_dia))

    def getID(self, x_loc, y_loc):
        if (x_loc, y_loc) in self.neurons_by_location.keys():
            return self.neurons_by_location[(x_loc, y_loc)]
        else:
            return None
    
    def getIDs(self):
        return self.neurons_by_id.keys()
    
    def getLocation(self, neuronID):
        if neuronID in self.neurons_by_id.keys():
            return self.neurons_by_id[neuronID]
        else:
            return None
            
    def getLocations(self):
        return self.neurons_by_location.keys()
    
    def getIDLocations(self):
        return self.ids_at_locations
    
    #This assumes a square neighborhood
    def getNeighbors(self, center, edge_len):
        #Convert to units of grid, input should be in um
        edge_len = int(edge_len/self.soma_dia)
        
        #The maximum and minimum indices of the x direction, with compensation for hitting the
        #edge of the grid. This assumes that there is no neuron to connect to off the edge of the
        #grid, which may be quite bogus. 
        max_x = min(self.cells_per_edge, center[0] + edge_len)
        min_x = max(0, center[0] - edge_len)
        max_y = min(self.cells_per_edge, center[1] + edge_len)
        min_y = max(0, center[1] - edge_len)
        
        #Stupid-fast compared to the previous iteration method.
        #Get a slice, flatten it, and strip everything that isn't negative, and so 
        #is a legit neuron ID. The map that's getting sliced is generated when the 
        #neuron IDs are assigned and the live locations are found.  
        neighborhood = self.ids_at_locations[min_x:max_x, min_y:max_y]
        neighborhood = neighborhood.flatten()
        neighbors = [x for x in neighborhood if x >= 0]
        
        return neighbors
     
    def getDistance(self, id1, id2):
        l1 = self.getLocation(id1)
        l2 = self.getLocation(id2)
        #Calculate distance. Grid units are soma diameters, so multiply by that to get real distance
        distance = math.sqrt((l1[0] - l2[0])**2 + (l1[1] - l2[1])**2)
        distance *= self.soma_dia
        return distance

    def euclidDist(self, p1, p2):    
        #Calculate distance. Grid units are soma diameters, so multiply by that to get real distance
        distance = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        distance *= self.soma_dia
        return distance

    #Given the x and y distance in um from the top left of the dish, 
    #return the location in grid coordinates     
    def um2coord(self, umX, umY):
        return (int(umX/soma_dia), int(umY/soma_dia))

    def getCellCount(self):
        return self.cellCount
    
    #Accept a set of neuron locations as an array where a -1 is no cell, and
    #any other value is a neuron ID
    def loadMaps(self, locations):
        self.neurons_by_location = {}
        self.neurons_by_id = {}
        self.ids_at_locations = locations
        x_max, y_max = locations.shape
        
        #Read the IDs and their locations into maps
        for x in xrange(0, x_max):
            for y in xrange(0, y_max):
                id = self.ids_at_locations[x][y]
                #We found a valid ID
                if id != -1:
                    self.neurons_by_id[id] = (x,y)
                    self.neurons_by_location[(x,y)] = id  
    
    def buildMaps(self, neuronPositions):
        #Build a map of cell locations to IDs, and IDs to cell locations
        self.neurons_by_location = {}
        self.neurons_by_id = {}
        self.ids_at_locations = np.negative(np.ones(neuronPositions.shape, dtype=np.int))
        
        neuron_id = 0
        for row_1 in xrange(self.cells_per_edge):
            for col_1 in xrange(self.cells_per_edge):
                if neuronPositions[row_1][col_1] == 1:
                    #If there is a neuron at the current position store its location
                    #and an ID, incrementing the ID
                    self.neurons_by_location[(row_1, col_1)] = neuron_id
                    self.neurons_by_id[neuron_id] = (row_1, col_1)
                    self.ids_at_locations[row_1, col_1] = neuron_id
                    neuron_id += 1
        #This also ended up counting the cells, so store that
        self.cellCount = neuron_id