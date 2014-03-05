#include "ros/ros.h"
#include "zanni/Channels.h"
#include "std_msgs/String.h"
#include "neuro_recv/dish_state.h"

ros::Publisher zanni_pub;
ros::Duration offset;

void translate(const zanni::Channels& msg) {

	//compose the new message
	neuro_recv::dish_state outMsg; 
	int jj = 0;
	//Copy the data over
	for (std::vector<double>::size_type ii = 0; ii != msg.voltages.size(); ++ii) {
		//Drop the corners
		if (ii == 0 || ii == 7 || ii == 56 || ii == 63){
			continue;
		}
		outMsg.samples[jj] = msg.voltages[ii];
		jj++;
	}

	//It's never the last dish
	outMsg.last_dish = 0;

	//It's the present dish
	outMsg.header.stamp = ros::Time::now() - offset;

	//ship it off
	zanni_pub.publish(outMsg);
}

int main(int argc, char **argv) {
	//Setup this node
	ros::init(argc, argv, "zanni_lvm_playback");
	ros::NodeHandle n;
	zanni_pub = n.advertise<neuro_recv::dish_state>("dish_states_to_burst_creator", 1000);

	//Load the input file specified in the yaml config
	std::string file_path;
	if(ros::param::get("/lvm_file_path", file_path))
	{
		printf("Got the file name %s\n", file_path);
	}


	//For timestamping the dish states
	offset = ros::Time::now() - ros::Time(0);

	ros::Rate r(1000); //run 1000 times a second
	while(ros::ok())
	{
		//
		ros::spinOnce();
		r.sleep();
	}
	return 0;
}
