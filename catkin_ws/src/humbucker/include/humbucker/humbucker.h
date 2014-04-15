#ifndef HUMBCUKER_H
#define HUMBUCKER_H

#include "ros/ros.h"
#include "neuro_recv/dish_state.h"

class Humbucker
{
public:
	Humbucker(){run();}
	void run();

private:
	void callback(const neuro_recv::dish_state::ConstPtr& dish);
	ros::NodeHandle n_;
	ros::Subscriber dish_state_sub_;
    ros::Publisher filtered_dish_pub_;
};
#endif
