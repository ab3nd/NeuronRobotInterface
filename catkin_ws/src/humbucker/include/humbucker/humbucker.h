#ifndef HUMBCUKER_H
#define HUMBUCKER_H

#include "ros/ros.h"
#include "neuro_recv/dish_state.h"
#include "Iir.h"
#include <vector>

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
    static const int order = 20;
    std::vector<Iir::Butterworth::BandStop < order, Iir::DirectFormI > > filter_bank;
};
#endif
