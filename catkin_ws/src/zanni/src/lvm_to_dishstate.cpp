#include "ros/ros.h"
#include "zanni/Channels.h"
#include "std_msgs/String.h"
#include "neuro_recv/dish_state.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <limits>
#include <cstdlib>

ros::Publisher zanni_pub;
ros::Duration offset;
std::ifstream lvm_file;

int main(int argc, char **argv) {
	//Setup this node
	ros::init(argc, argv, "zanni_lvm_playback");
	ros::NodeHandle n;
	zanni_pub = n.advertise < neuro_recv::dish_state > ("dish_states_to_burst_creator", 1000);

	//Load the input file specified in the yaml config
	std::string file_path;
	if (ros::param::get("/lvm_file_path", file_path)) {
		//Open the file
		lvm_file.open(file_path.c_str(), std::ios::out);
		//Skip the header lines at the beginning of the file
		for (int ii = 0; ii < 23; ++ii) {
			lvm_file.ignore(std::numeric_limits < std::streamsize > ::max(), '\n');
		}
	} else {
		ROS_ERROR("No lvm file specified.");
		ros::shutdown();
	}

	//For timestamping the dish states
	offset = ros::Time::now() - ros::Time(0);

	//For storing the current line of the file
	std::string current_line;
	std::string value;
	ros::Rate r(1000); //run 1000 times a second

	while (ros::ok()) {
		//get a line
		if (getline(lvm_file, current_line)) {
			//Convert to a stream and read off the first value, which is the timestamp
			std::istringstream line(current_line, std::istringstream::in);
			line >> value;

			//Read the rest of the values and stick them into a message
			neuro_recv::dish_state outMsg;
			int index = 0;
			double voltage = 0;
			while(line >> value)
			{
				//This only works because my lvm generation code generates atof()-friendly strings
				voltage = atof(value.c_str());
				outMsg.samples[index] = voltage;
				index++;
			}

			//It's never the last dish
			outMsg.last_dish = 0;

			//It's the present dish
			outMsg.header.stamp = ros::Time::now() - offset;

			//ship it off
			zanni_pub.publish(outMsg);
		}
		else
		{
			ROS_INFO("Done reading LVM file");
			lvm_file.close();
			ros::shutdown();
		}
		ros::spinOnce();
		r.sleep();
	}

	lvm_file.close();
	return 0;
}
