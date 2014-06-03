
#ifndef PATTERN_REC_H_
#define PATTERN_REC_H_

#include "ros/ros.h"
#include "neuro_recv/dish_state.h"
#include "burst_calc/buffer_spike_detector.h"

class PatternRec
{
public:

	PatternRec() { init(); }

private:
	void dish_recieved();
    void init();

	ros::NodeHandle n_;
    ros::Subscriber dish_state_sub_;


};


#endif