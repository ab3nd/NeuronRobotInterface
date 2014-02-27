#!/usr/bin/python
'''

Generates a connectivity map by simulating growth of seeded neuron cells. 

The growth simulation is a three-stage process:
1. Determine the cell density for each region of the MEA.
2. Assign cells to locations based on density. 
3. Connect the cells based on a connectivity function. 

Cell density is assigned based on random midpoint displacement fractals, aka "plasma fractals". 
This approach was chosen because it provides a stochastic approach that is computationally 
efficient. If it is not a good model of the actual distribution of neurons, a different algorithm
can be used. 

Cells are probabilistically assigned to locations based on the cell density (actually cell probability)
at that point. Cells are modeled as point locations. 

For each pair of cells, the probability of their connection is determined based on the distance 
between the cells and the cells are connected accordingly. Note that this results in N(N-1) comparisons, 
so roughly n^2 connections. Put that in your NP pipe and smoke it. 

'''
import math
import numpy as np
import networkx as nx
import pygame
from pickle import Pickler
import datetime
from brian import *
from brian.library.IF import *
import random
from pprint import pprint
import Image
import ConfigParser

import PhysicalDish
#Just for timing execution to find slow parts
from datetime import datetime
import cProfile
from brian.neurongroup import NeuronGroup

'''
Take a 2-D Numpy array and fill it in with a density map. The map values are in the range 
0-1 and describe the probability of there being a cell soma located at that location. 
1 is a cell, 0 is no cell. 
'''
def genPCell(density_map):
    #Assign a random value to each corner of the array
    max_x, max_y = density_map.shape
    random.seed()
    
    #Set corners to random values
    density_map[0][0] = random.random()
    density_map[max_x -1][0] = random.random()
    density_map[0][max_y - 1] = random.random()
    density_map[max_x-1][max_y-1] = random.random()
    
    #perform recursive plasma fractal generation
    squarePlasma(density_map)
    
def displace(size, originalSize):
    max = (float(size)/float(originalSize)) * 3.00
    displacement = (random.random() - 0.5) * max
    return displacement

def squarePlasma(array):
    
    if array.shape[0] < 3 and array.shape[1] < 3:
        return
    
    #Calculate midpoint values
    height, width = array.shape
    array[height/2][width-1] = (array[0][width-1] + array[height-1][width-1])/2
    array[height/2][0] = (array[0][0] + array[height-1][0])/2
    array[0][width/2] = (array[0][0] + array[0][width-1])/2
    array[height-1][width/2] = (array[height-1][0] + array[height-1][width-1])/2
    
    #Calculate center value
    center = 0
    center += array[height/2][width-1]
    center += array[height/2][0]
    center += array[0][width/2]
    center += array[height-1][width/2]
    center = center/4
    #Add displacement
    center += displace(height+width, 257*2)
    if center > 1:
        center = 1
    if center < 0:
        center = 0;
    #Set center value 
    array[height/2][width/2] = center
    
    #perform this step on sub-arrays
    squarePlasma(array[0:height/2+1,0:width/2+1])
    squarePlasma(array[0:height/2+1,width/2:width])
    squarePlasma(array[height/2:height,0:width/2+1])
    squarePlasma(array[height/2:height,width/2:width])
    
'''
Find the next highest power of two, to get a shape that's good for
plasma fractal generation 
'''      
def nextPowTwo(start):
    y = math.floor(math.log(start,2))
    return int(math.pow(2, y+1))

'''
Calculate the probability of a connection between two neurons, 
based on their distance apart.  
Generates a value from 0 to 1, centered at 
'''
def gaussConnect(distance, center):
    return math.e - ((distance - center)**2)/(2*center/2)**2

'''
Use pygame to rimport PhysicalDishender an array. The result is an image of the same dimensionality as the
array, with each pixel set to 255*the value of the corresponding array location. 
'''
def renderMap(densityData, title, renderPads=True):
    if densityData.ndim != 2:
        print "Can only render 2-D arrays"
    
    
    #Display the image
    win = pygame.display.set_mode(densityData.shape)
    win.fill((0,0,0))
    pygame.display.set_caption(title)
    screen = pygame.display.get_surface()
    color = densityData * 255
    color = color.astype(int)
    pygame.surfarray.blit_array(screen, color)
    
    #Draw a square the width and height of the area where the 
    #electrodes are 
    # Assumes: 8x8 pad array, 200um between pads
    #          1 pixel is a soma-width area, 30um across
    areaWidth = (8 * 200)/30
    left = densityData.shape[0]/2 - areaWidth/2
    top = densityData.shape[1]/2 - areaWidth/2
    if renderPads:
        pygame.draw.rect(screen, (200,0,0), pygame.Rect(left, top, areaWidth, areaWidth), 2)
    
    pygame.display.flip()
        
        
    #Write the array to an image
    #pic = Image.fromarray(color.astype(float))
    pic = Image.fromarray(pygame.surfarray.array3d(screen))
    pic.convert('RGB').save("{0}.png".format(title), "PNG")
    
    while 1:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                return

def grimReap(density_map, survival_rate):
    #For each cell, give it a survival_rate % chance of getting killed
    x_max, y_max = density_map.shape
    for ii in xrange(0,x_max):
        for jj in xrange(0, y_max):
            if random.random() > survival_rate/100.00:
                density_map[ii][jj] = 0

''' 
trim the number of existing cells to match the expected number of cells,
which is based on the density of cells in the plated solution
'''                
def densityReap(density_map, expected_cells):
    #Count the cells
    total_cells = countCells(density_map)
    #Decrease the surplus population
    surplus = total_cells - expected_cells
    print "total: ", total_cells
    print "expected: ", expected_cells
    print "surplus: ", surplus
    x_max, y_max = density_map.shape
    #Pick a random location in the dish, and if there is a cell there,
    #kill it. Repeat until the surplus population is gone
    while surplus > 0:
        #pick a random location
        rand_X = random.randint(0,x_max-1)
        rand_Y = random.randint(0,y_max-1)
        if density_map[rand_X][rand_Y] == 1:
            density_map[rand_X][rand_Y] = 0
            surplus -= 1

'''
Count the number of cells in the density map. Only works if the map contains
a 1 for live locations and 0 for empty locations. 
'''
def countCells(density_map):
    #Count the cells
    total_cells = 0
    for cell in density_map.flat:
        total_cells += cell
    return total_cells

# Based on "Dynamic Changes in Neural Circuit Topology Following Mild Mechanical Injury In Vitro"
# Tapan P. Patel, Scott C. Ventre, David F. Meaney
def getDegree(average):
    return np.random.poisson(average)

#Given an image, convert it to an appropriately sized map of cell locations, each of which 
#contains the probability that that location has a cell in it.  
def imgToProbability(imgPath, density_map):
    # Load image
    img = Image.open(imgPath)
    
    # Resize to match density map size
    size = density_map.shape
    img = img.resize(size, Image.ANTIALIAS)
    
    # select red color plane
    R,G,B = img.split()
    redPlane = np.array(R)
    
    #The full slices cause it to operate on the data in the array, 
    #rather than on a copy.    
    density_map[:] = redPlane
    density_map[:] = density_map/255.0
        
def main():
    
    config = ConfigParser.ConfigParser()
    config.readfp(open("./basic_sim.cfg"))
    
    phys_dish = PhysicalDish.PhysicalLayout(config)
    
    #Cell connectivity, as percentage of total connections
    connectivity_rate = config.getfloat("growth", "connectivity_rate")
    #Axon growth, needed to calculate connectivity
    axon_growth = config.getfloat("neuron", "axon_max_len")
    soma_dia = config.getfloat("neuron", "soma_diameter")
    #Cell density in cells/mm^2
    cell_density = config.getint("plating", "cell_density")
    #Cell survival rate, as percentage of plated cells
    survival_rate = config.getfloat("growth", "survival_rate")

    
    density_map = np.zeros((phys_dish.cells_per_edge, phys_dish.cells_per_edge))
    
    #If the user specified an image to control the cell density, load that
    #otherwise, calculate the cell density based on a plasma fractal 
    try:
        layoutFilePath = config.get ("plating", "dist_layout")
        layoutFilePath = str(layoutFilePath).strip('"\'')
        imgToProbability(layoutFilePath, density_map) 
    except ValueError:
        print "No layout specified, generating..."
        #Calculate cell distribution probability using plasma fractals
        genPCell(density_map)
    
    #Get the probability of a space having a cell, based on the cell density
    expected_cells = (phys_dish.dish_width/1000)**2 * cell_density
    possible_cells = phys_dish.cells_per_edge**2
    p_cell = float(expected_cells)/float(possible_cells)
    
    #Convert probabilities of cells into presence or absence
    #Iterating the data (e.g "for row in density_map") gets 
    #copies, iterating the indexes gets references
    for row in xrange(phys_dish.cells_per_edge):
        for col in xrange(phys_dish.cells_per_edge):
            if random.random() < density_map[row][col]:
            #if density_map[row][col] < p_cell:
                density_map[row][col] = 1
            else:
                density_map[row][col] = 0
    
    #Reap cells to configured density
    #Convert to mm^2 and multiply by density to get expected value
    densityReap(density_map, expected_cells)
    
    #Kill off some percentage of the cells to reflect cell death. 
    #Can lose 45-55% of the cells by 17 days in vitro, which is about the mature level
    grimReap(density_map, survival_rate)
    
    #Build the maps of cell location to ID and ID to cell location
    phys_dish.buildMaps(density_map)
                    
    #Calculate connections
    #Connections are stored as a list of tuples, (from neuron, to neuron)
    print "Building connectivity...",

    #Now have a list of neurons, their locations, and their IDs. Run through it 
    #and connect the neurons based on pairwise probability of connection
    conn_list = []
    
    for neuronID in phys_dish.getIDs():
        #Get the out-degree of this neuron, that is, how many neurons it connects to
        outConnect = getDegree(config.getfloat("neuron", "avg_out_degree"))
        
        #Get the physical location of this neuron
        neuron_location = phys_dish.getLocation(neuronID)
        
        #Get the neighborhood of neurons it could possibly be connected to
        #Half of the he length of an edge of the neighborhood is the maximum length of an axon,
        #measured in units of soma diameters (grid cells). It is half because the axon could
        #reach in either direction, so a full edge is 2*axon_growth.
        hood_edge_max = axon_growth*2
        
        #Start with a small neighborhood, size based on out-degree 
        current_hood = outConnect *2
        
        #Until either the hood has gotten as big as it can, or we're out of connections
        while current_hood < hood_edge_max and outConnect > 0:
            neighbors = phys_dish.getNeighbors(neuron_location, current_hood)
            
            #Sort the neurons based on distance from the current neuron
            def sortFunc(neuronA, neuronB):
                distA = phys_dish.getDistance(neuronID, neuronA)
                distB = phys_dish.getDistance(neuronID, neuronB)
                return cmp(distA, distB)
            neighbors.sort(sortFunc)
            
            for id in neighbors:
                distance = phys_dish.getDistance(neuronID, id)
                if random.random() < gaussConnect(distance, axon_growth):
                    #Just note that they are connected
                    conn_list.append((id, neuronID))
                    #Uses one of the out-degree, so drop that by one, once all the out-degree connections are used up,
                    #this neuron forms no more outgoing connections. 
                    outConnect = outConnect -1
                    #print "{0} connections left".format(outConnect)
                    if outConnect == 0:
                        break    
            
            #Didn't get all connections in smaller neighborhood, increase neighborhood size
            #for the next iteration. This will give closer neurons multiple chances to connect.
            #I'm unsure if this will be a bug or not.  
            if outConnect > 0:
                current_hood += outConnect * 3
                #print "{0} x {0}, {1} connections left".format(current_hood, outConnect)
                
    print "done."
        
    #Done building terrible huge list with a time consuming process. Pickle the results.
    print "Saving connectivity...", 
    now = datetime.now()
    file_date = "{0}-{1}-{2}-{3}:{4}:{5}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    file_date_short = "{0}/{1}/{2}".format(now.year, now.month, now.day)
    file_time = "{0}:{1}:{2}.{3}".format(now.hour, now.minute, now.second, now.microsecond)
    #file_time_short = "{0}:{1}".format(now.hour, now.minute)
    
    #Build a networkx graph
    conn_graph = nx.DiGraph()
    for connection in conn_list:
        conn_graph.add_edge(connection[0], connection[1])
    
    #Save the networkx graph
    with open("./nx_graph_{0}.pickle".format(file_date), "w") as outfile:
        Pickler(outfile, 0).dump(conn_graph)
        outfile.close()

    #Save the connectivity list
    with open("./connections_{0}.pickle".format(file_date), "w") as outfile:
        Pickler(outfile, 0).dump(conn_list)
        outfile.close()
    
    with open("./locations_{0}.pickle".format(file_date), "w") as outfile:
        Pickler(outfile, 0).dump(phys_dish.getIDLocations())
        outfile.close()
        
    print "done."
    
                
if __name__ == '__main__':
    main()
    
