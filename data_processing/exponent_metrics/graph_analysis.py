# Analyze a networkx graph to determine various graph-theoretical metrics 
# about it. Intended to discover small-world/scale-free networks. 

import argparse
import random
import networkx as nx
from pickle import Unpickler
from pprint import pprint
import os.path
from datetime import date

# Converts a list of connections of the form [(from, to), (from, to), ...] into
# a networkx network structure for structural analysis and graph theory
# jiggery-pokery to determine similarity with other networks
def conn2netx(infile):
    conn_graph = nx.DiGraph()
    connections = Unpickler(infile).load()
    for connection in connections:
        conn_graph.add_edge(connection[0], connection[1])
    return conn_graph
    
#Run through a list and count occurrences of each item,
#store them in a dictionary of items to counts
def bin(list):
    bins = {}
    for item in list:
        if item in bins.keys():
            bins[item] += 1
        else:
            bins[item] = 1
    return bins
            
#Get a dictionary of degrees to counts of nodes with that degree    
def getDegreeDist(graph):
    return bin(nx.degree(graph).values())

#Generate a connected random graph
#Start by adding a node and then selecting a node to connect it to
#If edges are left over, assign them to random pairs of nodes 
def genConnRandGraph(nodes, edges):
    rand_graph = nx.Graph()
    for nodeID in xrange(1,nodes):
        randEnd = random.randint(0, nodeID)
        rand_graph.add_edge(nodeID, randEnd)
    spare_edges = edges-nodes
    if spare_edges > 0:
        for edge in xrange(0, spare_edges):
            fromNode = random.randint(0, nodes)
            toNode = random.randint(0, nodes)
            rand_graph.add_edge(fromNode, toNode)
    return rand_graph

#Build a random graph with the same connectivity as the input graph
def buildRandom(graph):
    node_cnt = graph.number_of_nodes()
    edge_cnt = graph.number_of_edges()
    # Generate a random connected graph
    cmp_graph = genConnRandGraph(node_cnt, edge_cnt)
    return cmp_graph

#Build a random graph with as small a world as possible 
def buildSmallWorld(graph):
    node_cnt = graph.number_of_nodes()
    edge_cnt = graph.number_of_edges()
    # Barabasi-Albert graph is connected, is as small a world as possible
    cmp_graph = nx.barabasi_albert_graph(node_cnt, edge_cnt/node_cnt)
    return cmp_graph

def mfinderFormat(outGraph, outFileName):
    #Convert to a list of edges in the form of a tuple of node number for the originating node,
    #node number of the ending node, and a dictionary of edge attributes. I only care 
    #about the from and to nodes. 
    edgelist = nx.to_edgelist(outGraph)
    with open(outFileName, 'w') as outFile:
        for edge in edgelist:
            #The 1 at the end is a weight that mfinder expects, but does not use
            outFile.write("{0} {1} 1\n".format(edge[0], edge[1]))
        outFile.close()
    print "Wrote mfinder input file to {0}".format(outFileName) 
    
if __name__ == '__main__':
    #Get the file name
    parser = argparse.ArgumentParser(description="Analyze connectivity graphs")
    parser.add_argument("infile", metavar="input file", type=str, nargs=1, help="Path to file to analyze")
    
    args = parser.parse_args()
    
    with open(args.infile[0] + ".analysis", 'w') as logFile:
        #Load a directed graph from a file
        with open(args.infile[0], "r") as infile:
    
            logFile.write("Graph metrics for {0} generated on {1}\n\n".format(args.infile[0], date.today().strftime("%A %d. %B %Y") ))
            
            #Convert to networkx, and then build a random and small world graph with the same
            #number of nodes and edges to compare this graph to
            graph = conn2netx(infile)
            rnd_graph = buildRandom(graph)
            sml_graph = buildSmallWorld(graph)
                
            #Get the diameter of the graph and the comparison graphs
            '''
            if nx.is_connected(graph):
                diameter = nx.diameter(graph)
                rnd_diameter = nx.diameter(rnd_graph)
                sml_diameter = nx.diameter(sml_graph)
                logFile.write("Random graph diameter: {0}\n".format(rnd_diameter))
                logFile.write("Input network graph diameter: {0}\n".format(diameter))
                logFile.write("Small-world network graph diameter: {0}\n\n".format(sml_diameter))
            else:
                logFile.write("Graph is not connected, diameter is infinite\n\n")
            '''
                
            #Get characteristic path length of the graph and the comparison graphs
            avg_path = nx.average_shortest_path_length(graph)
            rnd_avg_path = nx.average_shortest_path_length(rnd_graph)
            sml_avg_path = nx.average_shortest_path_length(sml_graph)
            logFile.write("Random graph avg. shortest path: {0}\n".format(rnd_avg_path))
            logFile.write("Input network graph avg. shortest path: {0}\n".format(avg_path))
            logFile.write("Small-world network graph avg. shortest path: {0}\n\n".format(sml_avg_path))
                        
            #Clustering isn't supported for directed graphs (Y U NO DO THIS!?!)
            undir_g = nx.Graph(graph) 
            avg_clustering = nx.average_clustering(undir_g)
            rnd_avg_clustering = nx.average_clustering(rnd_graph)
            sml_avg_clustering = nx.average_clustering(sml_graph)
            logFile.write("Random graph avg. clustering: {0}\n".format(rnd_avg_clustering))
            logFile.write("Input network graph avg. clustering: {0}\n".format(avg_clustering))
            logFile.write("Small-world network graph avg. clustering: {0}\n\n".format(sml_avg_clustering))
            
            #Get the degree distribution of the graph
            #Should be power-law for a scale-free network
            degree_dist = nx.degree_histogram(graph)
            rnd_deg_dist = nx.degree_histogram(rnd_graph)
            sml_deg_dist = nx.degree_histogram(sml_graph)
        
            #Output degree histograms for gnuplot 
            outFName = args.infile[0] + ".gnuplot"
            print "Writing degree histograms to {0}...".format(outFName),
            with open(outFName, 'w') as outGnuplot:
                max_degree = max([len(degree_dist), len(rnd_deg_dist), len(sml_deg_dist)])
                for ii in xrange(0, max_degree):
                    graph_deg = 0
                    if ii < len(degree_dist):
                        graph_deg = degree_dist[ii]
                        
                    rnd_deg = 0 
                    if ii < len(rnd_deg_dist):
                        rnd_deg = rnd_deg_dist[ii]
                        
                    sml_deg = 0
                    if ii < len(sml_deg_dist):
                        sml_deg = sml_deg_dist[ii]
                        
                    outGnuplot.write("{3}\t{0}\t{1}\t{2}\n".format(graph_deg, rnd_deg, sml_deg, ii))
                outGnuplot.close()
            print "done."
            logFile.write("Wrote degree histograms to {0}\n".format(outFName))
            logFile.write("Plot using: plot \"{0}\" using 1:2 with lines title \"Simulation\", \"{0}\" using 1:3 with lines title \"Random\", \"{0}\" using 1:4 with lines title \"Small-World\"".format(outFName))
            
            #Generate output files for mfinder (http://www.weizmann.ac.il/mcb/UriAlon/)
            #which performs motif finding on graphs. The graph format is described in the 
            #comments for mfinderFormat()
            print "Writing mfinder input files...\n",
            outFName = args.infile[0] + ".mfinder_graph"
            mfinderFormat(graph, outFName)
            logFile.write("Wrote mfinder input file {0}".format(outFName))
            
            outFName = args.infile[0] + ".mfinder_random"
            mfinderFormat(graph, outFName)
            logFile.write("Wrote mfinder input file {0}".format(outFName))
            
            outFName = args.infile[0] + ".mfinder_smlwrld"
            mfinderFormat(graph, outFName)
            logFile.write("Wrote mfinder input file {0}".format(outFName))
            print "done."    
     