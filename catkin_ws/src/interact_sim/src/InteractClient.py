#!/usr/bin/python

import roslib; roslib.load_manifest('neuro_recv')
import rospy
from neuro_recv.msg import *
from brian import *
import numpy as np

if __name__ == '__main__':
     
    #Set this up as a ROS node 
    pub = rospy.Publisher('dish_states_to_burst_creator', dish_state)
    rospy.init_node('plate_sender')
    r = rospy.Rate(1000) #We send dishes fast
    
    #And a Brian client
    client = RemoteControlClient()
    
    #Get some values from the server
    pad_rows = client.evaluate('self.config.getint("mea", "pad_rows")')
    pad_cols = client.evaluate('self.config.getint("mea", "pad_cols")')
    map = client.evaluate('self.pad_neuron_map')
    
    #Get the time offset
    offset = rospy.Time.now() - rospy.Time(0)
    
    #Counter to figure out buffering
    count = 0
    
    while not rospy.is_shutdown():
        neuronVoltages = client.evaluate('self.culture.vm')
                
        #Set up an array of voltages
        pad_voltages = np.zeros(((pad_rows*pad_cols)))     
        #For every pad in the dish
        for pad in map.keys(): 
            neurons = map[pad]
            total = 0.0
            for neuron in neurons:
                #Sum of the membrane voltages of the neurons, multiplied by the inverse 
                #square of the distance from the pad to the neuron. 
                try:
                    total += 1/((neuron[1] + 1) **2) * neuronVoltages[neuron[0]]
                except:
                    import pdb; pdb.set_trace()
                #The pads don't come out in a particular order, this reorders them
                pad_voltages[(pad[0] + pad[1]*pad_rows)] = total
        
        #Get rid of corners
        pad_voltages = np.delete(pad_voltages, [(pad_cols * pad_rows)-1, ((pad_cols * (pad_rows-1))), pad_rows-1, 0])
                 
        #Send off a plate message
        timeStamp = rospy.Time.now() - offset
        msg = dish_state(samples=pad_voltages, last_dish = False)
        msg.header.stamp = timeStamp
        pub.publish(msg)
        count += 1
        if count < 3000:
            if count % 100 == 0:
                print "Buffering {0}/3000".format(count)
        
            
        r.sleep()
        
        
        