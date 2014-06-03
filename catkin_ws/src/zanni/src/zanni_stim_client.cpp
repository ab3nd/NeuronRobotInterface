#include "ros/ros.h"
#include "zanni/Stim.h"
#include "sine.hpp"
#include <cstdlib>
#include <unistd.h>

int main(int argc, char **argv) {
	ros::init(argc, argv, "zanni_stim_client");

	ros::NodeHandle n;
	ros::ServiceClient client = n.serviceClient<zanni::Stim>("deliver_stim");

	zanni::Stim srv;

	for(int channel = 0; channel < 2; channel++)
	{
		srv.request.signal.clear();

//		//Fill in the service request with the data from the header file.
//		int elements = sizeof(tiny_sine)/sizeof(tiny_sine[0]);
//		for(int ii = 0; ii < elements; ii++)
//		{
//			//Multiply by 10000 because we're pushing +/-10V into a 10000-fold attenuation
//			//This way the input signals can still be in normal neuron signal range
//			srv.request.signal.push_back(tiny_sine[ii] * 10000);
//		}


			//Fill in the service request with the data from the header file.
			int elements = sizeof(training_signal)/sizeof(training_signal[0]);
			for(int ii = 0; ii < elements; ii++)
			{
				//Multiply by 10000 because we're pushing +/-10V into a 10000-fold attenuation
				//This way the input signals can still be in normal neuron signal range
				srv.request.signal.push_back(training_signal[ii] * 10000);
			}


		//Set up the channel
		srv.request.channel = channel;

		//Make the call
		if (client.call(srv)) {
			if(srv.response.done)
			{
				ROS_INFO("Stimulation sent");
			}
			else
			{
				ROS_WARN("Problem on stimulation end");
			}
		} else {
			ROS_ERROR("Failed to call stimulation");
			return 1;
		}

		sleep(1);
	}
	return 0;
}
