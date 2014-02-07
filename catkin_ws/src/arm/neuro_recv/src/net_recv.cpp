/*
 * neuro_recv.cpp
 *
 *  Created on: May 31, 2012
 *      Author: ams
 */

#include "ros/ros.h"
#include "neuro_recv/dish_state.h"
//#include "neuro_recv/sample.h"
#include "../../../common/PracticalSocket.h" // For UDPSocket and SocketException
#include <cstring>
#include <stdint.h>
#include <endian.h>

//#define DEBUG
#define WRITE_CSV

#ifdef WRITE_CSV
#include <fstream>
#endif

int main(int argc, char **argv) {
	ros::init(argc, argv, "neuro_recv");
	ros::NodeHandle n;

#ifndef WRITE_CSV
	ros::Publisher chatter_pub = n.advertise < neuro_recv::dish_state > ("dish_states_to_burst_creator", 1000);
#endif
	/*This is kind of a high rate, but there are 1k samples taken
	 * per second.
	 */
	ros::Rate loop_rate(1000);

	//Set up communication port
	unsigned short port = 6666; //local port
	unsigned char data[600];

#ifdef WRITE_CSV
	//Open the logfile for writing
	fstream outfile;
	//outfile.open("net_data_stream.csv", fstream::out | fstream::app);
	outfile.open("net_data_stream.csv", fstream::out);
#endif

	//Set up timing stuff
	// Initialize the time stamp offset
	ros::Duration offset = ros::Time::now() - ros::Time(0);

	try {

		ROS_INFO("Neuron data receiver waiting for connection...");
		//Wait to receive an incoming connection
		TCPServerSocket sock(port);
		TCPSocket *rcvSock = sock.accept();

		ROS_INFO("Neuron data receiver got a connection");

		//We'll need a place to store the data
		neuro_recv::dish_state msg;

		//Get the first set of data
		int len;
		len = rcvSock->recv(&data, sizeof(data));

		while (ros::ok()) {
			if (len > 0) {
				/* Detect packet start. The start sentinel is what LabView puts
				 * at the beginning of the packet, and is the number of values
				 * in the array as a 32-bit int. Note that changing the array
				 * size will change this. */
				uint32_t sentinel = 0x3c000000;
				uint start = 0;
				for (start = 0; start < sizeof(data) - sizeof(sentinel); start++) {
					//See if we found the start sentinel
					if (memcmp((void*) &data[start], (void*) &sentinel, sizeof(sentinel)) == 0) {
						//Set start to point just after sentinel
						start += sizeof(sentinel);
						break;
					}
				}

				//Calculate some offsets
				int moveBytes = sizeof(data) - start;
				int tailspace = sizeof(data) - moveBytes;

				//Shift the data up to the beginning of the array
				memmove((void*) &data, (void*) (&data[start]), moveBytes);

				//Receive some new data to fill in the tail of the array
				len = rcvSock->recv((void*) &data[moveBytes - 1], tailspace);

				/* Convert to doubles and store in a vector. MARG BAR TYPE PUNNING */
				//60 is a magic number for the number of channels
				int index = 0;
				for (uint ii = 0; ii < 60 * sizeof(uint64_t); ii += sizeof(uint64_t)) {
					uint64_t input;
					memcpy((void*) &input, (void*) &(data[ii]), sizeof(uint64_t));
					input = htobe64(input);
					double dbl = *reinterpret_cast<double*>(&input);
					msg.samples[index] = dbl;
#ifdef WRITE_CSV
					//Write the value to the log file
					if(index == 0){
						outfile << dbl;
					}
					else{
						outfile <<","<< dbl;
					}
#endif
					index++;
				}

#ifdef DEBUG
				ROS_INFO("Dish values:");
				ROS_INFO("\t %f %f %f %f %f %f \t", msg.samples[0], msg.samples[1], msg.samples[2], msg.samples[3], msg.samples[4], msg.samples[5]);
				for (int row = 6; row < 50; row = row + 8) {
					ROS_INFO("%f %f %f %f %f %f %f %f", msg.samples[row + 0], msg.samples[row + 1], msg.samples[row + 2], msg.samples[row + 3], msg.samples[row + 4], msg.samples[row + 5], msg.samples[row + 6], msg.samples[row + 7]);
				}
				ROS_INFO("\t %f %f %f %f %f %f \t", msg.samples[54], msg.samples[55], msg.samples[56], msg.samples[57], msg.samples[58], msg.samples[59]);
#endif
#ifdef WRITE_CSV
				outfile << endl;
#endif

			}

			msg.header.stamp = ros::Time::now() - offset;

			//Publishing is suppressed if we are writing CSV. The CSV reader should be doing the reading from a file
#ifndef WRITE_CSV
			chatter_pub.publish(msg);
#endif
			ros::spinOnce();

			//Not sleeping results in publishing states too fast.
			loop_rate.sleep();
		}

	} catch (SocketException &e) {
		ROS_ERROR("%s", e.what());
		exit(1);
	}

#ifdef WRITE_CSV
	outfile.close();
#endif

	return 0;
}
