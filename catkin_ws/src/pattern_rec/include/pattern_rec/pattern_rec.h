
#ifndef PATTERN_REC_H_
#define PATTERN_REC_H_

#include "ros/ros.h"

class PatternRec
{
public:

private:
	void dish_recieved();
    void init();

	ros::init(argc, argv, "Pattern_Seer");
	ros::NodeHandle n_;
    ros::Subscriber dish_state_sub_;

	ros::spin();


}