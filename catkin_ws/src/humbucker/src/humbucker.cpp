/*
 * Receives dish states and applies a 60Hz noise filter to them.
 * Emits dish states, with everything at 60Hz missing.
 */

#include "humbucker/humbucker.h"


void Humbucker::callback(const neuro_recv::dish_state::ConstPtr& d)
{
	//New dish to send out
	neuro_recv::dish_state filtered_dish;
	//Filter using the filter bank. Each channel has its own filter
	for (int ii = 0; ii < 60; ii++)
	{
		filtered_dish.samples[ii] = filter_bank[ii].filter(d->samples[ii]);
	}

	filtered_dish_pub_.publish(filtered_dish);
	ROS_INFO("Humbucker published a state.");
}

void Humbucker::run()
{
	// Set up 60 filters, one for each input pad of the dish
	// bandstop filter, centered at 60, width of 3
	const float samplingrate = 1000; //Hz AKA samples/second
	const float center_frequency = 60; //Hz, AKA USA power line noise
	const float frequency_width = 5;
	for(int ii = 0; ii < 60; ii++)
	{
		Iir::Butterworth::BandStop < order, Iir::DirectFormI > bs;
		bs.setup(order, samplingrate, center_frequency, frequency_width);
		bs.reset();
		filter_bank.push_back(bs);
	}

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
