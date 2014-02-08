/*
 * mock_recv.cpp
 *
 *  Created on: March 10, 2013
 *      Author: ams
 */

#include "ros/ros.h"
#include "neuro_recv/dish_state.h"
#include <cstring>
#include <stdint.h>
#include <endian.h>

#define DEBUG

int main(int argc, char **argv) {
	ros::init(argc, argv, "neuro_recv");
	ros::NodeHandle n;
	ros::Publisher chatter_pub = n.advertise < neuro_recv::dish_state > ("dish_states_to_burst_creator", 1000);

	ros::Rate loop_rate(1000);

	//Set up timing stuff
	// Initialize the time stamp offset
	ros::Duration time_offset = ros::Time::now() - ros::Time(0);


		ROS_WARN("Fake data receiver generating data");

		//We'll need a place to store the data
		neuro_recv::dish_state msg;

		//Limit on fake data
		double limit = 0.003;

		while (ros::ok()) {
				/* Generate fake data and use that */
				//60 is a magic number for the number of channels
				for (uint ii = 0; ii < 60; ii++) {
					double volt_offset = ((double)(rand() % 600) - 300)/1000000.0;

					//Don't exceed limit
					if (abs((double)msg.samples[ii] + volt_offset) > limit)
					{
						volt_offset = -volt_offset;
					}

					msg.samples[ii] += volt_offset;
				}

#ifdef DEBUG
				ROS_INFO("Dish values:");
				ROS_INFO("\t %f %f %f %f %f %f \t", msg.samples[0], msg.samples[1], msg.samples[2], msg.samples[3], msg.samples[4], msg.samples[5]);
				for (int row = 6; row < 50; row = row + 8) {
					ROS_INFO("%f %f %f %f %f %f %f %f", msg.samples[row + 0], msg.samples[row + 1], msg.samples[row + 2], msg.samples[row + 3], msg.samples[row + 4], msg.samples[row + 5], msg.samples[row + 6], msg.samples[row + 7]);
				}
				ROS_INFO("\t %f %f %f %f %f %f \t", msg.samples[54], msg.samples[55], msg.samples[56], msg.samples[57], msg.samples[58], msg.samples[59]);
#endif

			msg.header.stamp = ros::Time::now() - time_offset;

			chatter_pub.publish(msg);

			ros::spinOnce();

			//Not sleeping results in publishing states too fast.
			loop_rate.sleep();
		}

	return 0;
}
