/*
 * slicerTest.cpp
 *
 *  Created on: Jun 27, 2012
 *      Author: ams
 */

#include "ros/ros.h"
#include <stdint.h>
#include "img_slicer/ImageSlicer.h"
#include "common_libs/PracticalSocket.h"
#include <plotter.h>
#include <vector>
#include <cstdlib>
#include <endian.h>

#define P_WIDTH 720
#define P_HEIGHT 480

XPlotter* setupDisplay() {
	PlotterParams plotter_params;
	//Set up width and height
	ostringstream oss;
	oss << P_WIDTH << "x" << P_HEIGHT;
	plotter_params.setplparam("BITMAPSIZE", (void*) oss.str().c_str());
	plotter_params.setplparam("USE_DOUBLE_BUFFERING", (char *) "yes");

	/* create an X Plotter with the specified parameters */
	XPlotter *plotter = new XPlotter(stdin, stdout, stderr, plotter_params);

	if (plotter->openpl() < 0) /* open Plotter */
	{
		ROS_ERROR("Couldn't open Plotter");
		return NULL;
	}

	plotter->space(0, 0, P_WIDTH, P_HEIGHT); //coordinates in pixels, not (0,0)-(1,1)
	plotter->flinewidth(0.01); //line thickness
	plotter->filltype(1); //Fill objects
	plotter->bgcolor(0, 0, 0); //Black, colors are RGB, 16 bits/channel
	plotter->erase();

	return plotter;
}

uint16_t valueMap(uint64_t input, uint min_in, uint max_in, int min_out,
		int max_out) {
	uint16_t retVal = 0;
	//constrain to the range
	if (input > max_in) {
		input = max_in;
	} else if (input < min_in) {
		input = min_in;
	}

	//map the constrained value into the range
	retVal = (uint16_t) ((input - min_in) * (max_out - min_out)
			/ (max_in - min_in) + min_out);
	return retVal;
}

int redrawDisplay(XPlotter* plotter, vector<uint64_t> counts) {
	int segments = counts.size();
	//Dividing by zero will END ALL. ZALGO!
	if (segments == 0) {
		ROS_ERROR("Got no segments.");
		return 1;
	}
	int segWidth = P_WIDTH / segments;

	for (int ii = 0; ii < segments; ii++) {
		uint16_t red = 0;
		red = valueMap(counts[ii], 0, segWidth * P_HEIGHT, 0, 65536);
		uint16_t green = 0;
		uint16_t blue = 0;
		plotter->color(red, green, blue);
		plotter->box((ii * segWidth), 0, ((ii + 1) * segWidth), P_HEIGHT);
	}
	plotter->erase();
	return 0;
}

int sendLabview(const vector<uint64_t>* counts, TCPSocket* sock) {

	/*Start simple: Send 0xDEADBEEF
	unsigned int bufferSize = sizeof(uint32_t);
	void* outBytes = std::malloc(bufferSize);
	if (NULL == outBytes) {
		ROS_ERROR("Could not allocate memory for data to send");
		return 1;
	}

	uint32_t toSend = 0xDEADBEEF;
	uint32_t output = htobe32(toSend);
	std::memcpy(outBytes, (void*)&output, sizeof(uint32_t));

	try {
		sock->send(outBytes, sizeof(outBytes));
	} catch (SocketException &e) {
		ROS_ERROR("Socket exception wile sending: %s\n", e.what());
	}
	return 0;
	*/

	/* Get a chunk of memory to hold the counts and the size of the
	 * array. This chunk will become what gets sent to Labview.
	 */
	if (counts->size() > 0) {
		//Sentinel, array size, and the array
		unsigned int bufferSize = sizeof(uint32_t) * 2
				+ (sizeof(uint64_t) * counts->size());
		void* outBytes = std::malloc(bufferSize);
		if (NULL == outBytes) {
			ROS_ERROR("Could not allocate memory for data to send to labview");
			return 1;
		}
		//Keep an index to where we are writing
		void* index = outBytes;

		/* Translate the size of the vector into a 32-bit int
		 * This is prepended to the beginning of the Labview-format array, as its size.
		 * It is a uint because negative size is nonsensical
		 */
		uint32_t sentinel = htobe32(0xdeadbeef);
		std::memcpy(index, (const void*) &sentinel, sizeof(sentinel));
		index += sizeof(sentinel);
		uint32_t countSize = counts->size() * sizeof(uint64_t);
		countSize = htobe32(countSize);
		std::memcpy(index, (const void*) &countSize, sizeof(countSize));
		index += sizeof(countSize);


		for (vector<uint64_t>::const_iterator countIt = counts->begin();
				countIt < counts->end(); ++countIt) {
			uint64_t output = htobe64(((uint64_t)*countIt));
			std::memcpy(index, (const void*) &output, sizeof(output));
			index += sizeof(output);
		}

		/* Print out for debugging purposes
		index = outBytes;
		for (uint ii = 0; ii < bufferSize; ii++) {
			printf("%02x ", *((uint8_t*) index));
			index += sizeof(uint8_t);
		}
		printf("\n\n");
		//*/

		//Attempt to send the data
		try {
			sock->send(outBytes, bufferSize);
		} catch (SocketException &e) {
			ROS_ERROR("Socket exception wile sending: %s\n", e.what());
			ros::shutdown();
		}
		return 0;
	}
	return 1;
}

int main(int argc, char** argv) {
	// Set up ROS.
	ros::init(argc, argv, "slice_client");
	ros::NodeHandle n;

	// Initialize node parameters from launch file or command line.
	// Use a private node handle so that multiple instances of the node can be run simultaneously
	// while using different parameters.
	ros::NodeHandle private_node_handle_("~");

	//Set up the client
	ros::ServiceClient sliceClient = n.serviceClient<img_slicer::ImageSlicer>(
			"red_px_counts");

	//Rate to loop in Hz
	ros::Rate r(10);

	//Run in a loop forever, making requests
	img_slicer::ImageSlicer srv;
	srv.request.slices = 5;

	//Set up plotter for visualization
	XPlotter* plot = setupDisplay();

	//Set up socket for transmission
	string address = "129.63.153.120";
	unsigned short port = 6667;

	try {
		TCPSocket sock(address, port);
		while (n.ok()) {
			if (sliceClient.call(srv)) {
				redrawDisplay(plot, srv.response.pixelCount);
				sendLabview(&srv.response.pixelCount, &sock);
			} else {
				ROS_ERROR("Call failed");
			}

			r.sleep();
		}
	} catch (SocketException &e) {
		ROS_ERROR("Socket exception %s\n", e.what());
		while (n.ok()) {
			if (sliceClient.call(srv)) {
				redrawDisplay(plot, srv.response.pixelCount);
			} else {
				ROS_ERROR("Call failed");
			}

			r.sleep();
		}

	}

	return 0;
}
