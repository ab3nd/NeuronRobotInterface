#!/usr/bin/python
from pickle import Unpickler, Pickler
import argparse
import re
import random
import os

if __name__ == "__main__":
    argp = argparse.ArgumentParser(description='Draw an image based on connection and layout files')
    argp.add_argument('-c', dest='conn_path')
    args = argp.parse_args()
    
    #Get the connection file name
    conn_file = args.conn_path
    #Derive the location file name
    loc_file = re.sub("connections", "locations", args.conn_path)
     
    #Load the input files. This should eventually be done from the command line
    with open(conn_file) as infile:
        connections = Unpickler(infile).load()
        infile.close()
    
    with open(loc_file) as infile:
        locations = Unpickler(infile).load()
        infile.close()

    #Build an index of IDs to locations
    idToLoc = {}
    for x in range(0, locations.shape[0]):
        for y in range(0, locations.shape[1]):
            if locations[x,y] > -1:
                idToLoc[locations[x,y]] = (x,y) 
    
    #The middle line is along the X axis, in the center
    middle = locations.shape[0]/2
    
    #Set the quality of the cut, from 10-100 in steps of 10
    #pCut=100 means a 100 percent chance of cutting all candidate connections 
    for pCut in xrange(10, 110, 10):
        
        #Set up a new output file name
        outputFile = "cut_p{0}_{1}".format(pCut, os.path.basename(args.conn_path))
        newConnections = []
        
        #Split the connections
        for connection in connections:
            x1 = idToLoc[connection[0]][0]
            x2 = idToLoc[connection[1]][0]
            if (x1 > middle and x2 < middle) or (x2 > middle and x1 < middle):
                #Candidate for severing
                if(random.random() * 100 < pCut):
                    #Break the connection
                    print "Breaking connection from {0} to {1}".format(idToLoc[connection[0]], idToLoc[connection[1]])
                else:
                    #Leave it in
                    newConnections.append(connection)
            else:
                #Not a candidate for severing
                newConnections.append(connection)
        
        #Save the new connection file
        with open(outputFile, 'w') as outfile:
            Pickler(outfile).dump(newConnections)
            outfile.close()
        