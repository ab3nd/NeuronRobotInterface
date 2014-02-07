/*
 * slicerTest.cpp
 *
 *  Created on: Jun 27, 2012
 *      Author: ams
 */

#include "ros/ros.h"
#include <stdint.h>
#include "img_slicer/ImageSlicer.h"
#include <plotter.h>
#include <vector>
#include <cstdlib>
#include <cmath>
#include <endian.h>
#include "zanni/Stim.h"
#include "sine.hpp"

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

uint16_t valueMap(uint64_t input, uint min_in, uint max_in, int min_out, int max_out) {
	uint16_t retVal = 0;
	//constrain to the range
	if (input > max_in) {
		input = max_in;
	} else if (input < min_in) {
		input = min_in;
	}

	//map the constrained value into the range
	retVal = (uint16_t) ((input - min_in) * (max_out - min_out) / (max_in - min_in) + min_out);
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

int main(int argc, char** argv) {
	// Set up ROS.
	ros::init(argc, argv, "slice_client");
	ros::NodeHandle n;

	// Initialize node parameters from launch file or command line.
	// Use a private node handle so that multiple instances of the node can be run simultaneously
	// while using different parameters.
	ros::NodeHandle private_node_handle_("~");

	//Set up the clients, one to call for slices, the other to order stims
	ros::ServiceClient sliceClient = n.serviceClient<img_slicer::ImageSlicer>("red_px_counts");
	ros::ServiceClient stimClient = n.serviceClient<zanni::Stim>("deliver_stim");

	//Rate to loop in Hz
	ros::Rate r(10);

	//Run in a loop forever, making requests
	img_slicer::ImageSlicer srv;
	srv.request.slices = 5;

	//Set up plotter for visualization
	XPlotter* plot = setupDisplay();

	//Run in a loop making the calls
	while (n.ok()) {
		if (sliceClient.call(srv)) {
			redrawDisplay(plot, srv.response.pixelCount);

			uint64_t leftCount = 0;
			uint64_t rightCount = 0;
			for (int ii = 0; ii < 3; ii++) {
				leftCount += srv.response.pixelCount[ii];
				rightCount += srv.response.pixelCount[4 - ii];
			}
			ROS_INFO("R: %u L: %u\n", leftCount, rightCount);
			//Don't bother stimulating at all unless difference is big
			if (abs(leftCount - rightCount) > 500) {

				//Fill in the service request with the data from the header file.
				zanni::Stim stimSrv;
				int elements = sizeof(training_signal) / sizeof(training_signal[0]);
				for (int ii = 0; ii < elements; ii++) {
					stimSrv.request.signal.push_back(training_signal[ii]);
				}

				//Pick a channel
				if (leftCount > rightCount) {
					stimSrv.request.channel = 0; //Arbitrary decision that 0 = left
				} else {
					stimSrv.request.channel = 1;
				}

				//Make the call
				if (stimClient.call(stimSrv)) {
					if (stimSrv.response.done) {
						ROS_INFO("Stimulation sent");
					} else {
						ROS_WARN("Problem on stimulation end");
					}
				} else {
					ROS_ERROR("Failed to call stimulation");
					return 1;
				}

			}

		} else {
			ROS_ERROR("Call failed to get pixel counts");
		}

		r.sleep();
	}
	return 0;
}
