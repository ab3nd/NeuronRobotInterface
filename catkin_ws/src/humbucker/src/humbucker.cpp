/*
 * Receives dish states and applies a 60Hz noise filter to them.
 * Emits dish states, with everything at 60Hz missing.
 */

#include "humbucker/humbucker.h"

void Humbucker::callback(const neuro_recv::dish_state::ConstPtr& d)
{
	//Do nothing, just republish it
	filtered_dish_pub_.publish(d);
	ROS_INFO("Humbucker published a state.");
}

void Humbucker::run()
{
	//Wait for a subscriber
	filtered_dish_pub_ = n_.advertise<neuro_recv::dish_state>("filtered_dish_states", 1);
    ROS_INFO("Humbucker waiting for subscribers...");
    while((filtered_dish_pub_.getNumSubscribers() < 1) && ros::ok());
    ROS_INFO("Humbucker got a subscriber.");

	// Subscribe to dish states
	dish_state_sub_ = n_.subscribe("dish_states_to_burst_creator", 1000, &Humbucker::callback, this);

    while (ros::ok())
    {
        ros::spinOnce();
    }
}

int main(int argc, char** argv)
{
	// Init the node
	ros::init(argc, argv, "humbucker");

	// Launch it (constructor calls run())
	Humbucker h;
	//h.run();

	return 0;
}
