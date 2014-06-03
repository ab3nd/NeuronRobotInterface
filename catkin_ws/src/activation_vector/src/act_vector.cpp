/*
 * Receives dish states from a program that reads the MEA amplifier.
 * Outputs motion commands to the arm.
 *
 * TODO A lot of the messaging stuff from this, and the other nodes in arm_project/,
 * should be consolidated and ported to catkin rather than rosbuild.
 */
#include "act_vector/act_vector.h"
//The number e, for exponetial decay
#define E (2.7182818284590452353602874713526624977572470937L)
//Decay constant, expressed as the reciprocal of frames per second
#define BETA (1.0/1000.0)
//Used in normalization
#define SIGMA (0.1)



double ActVector::euclidianDistance(double a[], const double* b)
{
	double total = 0;
	for (int ii = 0; ii < 60; ii++)
	{
		total += pow((a[ii] - b[ii]),2);
	}
	return sqrt(total);
}
void ActVector::callback(const neuro_recv::dish_state::ConstPtr& d)
{


    if(buf_.isBuffered())
	{
		//Check for spikes
		for (int ii = 0; ii < 60; ii++)
		{
			//TODO is this only looking at positive-going spikes?
			if(d->samples[ii] > buf_.getThreshold(ii))
			{
				//Decay and add one
				activation_[ii] = activation_[ii] * pow(E, -BETA*(frameCounter - lastFrame[ii])) + 1;
				lastFrame[ii] = frameCounter;
			}
			else
			{
				//Just decay
				activation_[ii] = activation_[ii] * pow(E, -BETA*(frameCounter - lastFrame[ii]));
			}
		}

		//Debugging printf as a CSV data stream
//		printf("%f", activation_[0]);
//		for(int ii = 1; ii < 60; ii++)
//		{
//			printf(",%f", activation_[ii]);
//		}
//		printf("\n");

		frameCounter++;
	}
	else
	{
		buf_.add(*d);
	}
}

void ActVector::run()
{

    if(!ros::ok())
        {
            ROS_INFO("Test to stop the arm!");
            
        
                        // Everything else is 0 (doesn't move)
            arm::constant_move stop;
            stop.speeds.fill(static_cast<int8_t>(0));
            stop.states[Z] = 0;
            stop.states[YAW] = 0;
            stop.states[PITCH] = 0;
            stop.states[ROLL] = 0;
            stop.states[GRIP] = 0;
            stop.states[LIFT] = 0;
            cmd_pub_.publish(stop);
        }

    while (ros::ok())
    {
        ros::spinOnce();

        int x = 1;
        
        if((ros::Time::now() - lastSent > ros::Duration(0.2)) && buf_.isBuffered()){
        	lastSent = ros::Time::now();

        	//Normalize the activation vector
        	for(int ii = 0; ii < 60; ii++)
        	{
        		normActivation_[ii] = tanh(SIGMA * activation_[ii]);
        	}

        	//Compare this activaton vector to the known ones
        	float leftDist = euclidianDistance(normActivation_, action::lAct);
        	float rightDist = euclidianDistance(normActivation_, action::rAct);

        	//printf("%f,%f,%f\n", leftDist, rightDist, fabs(leftDist-rightDist));

        	//This is an empirically derived parameter, but should hold thanks to normalization
        	if(fabs(leftDist-rightDist) > 0.2)
        	{
            	//Send the appropriate move
            	arm::constant_move cmd;
            	//TODO set up the end time? Fucking time server.
            	if(leftDist > rightDist)
            	{
            		ROS_INFO("More activity on left, moving LEFT.");
            		cmd.states[Y] = ARM_LEFT;
            	}
            	else
            	{
            		ROS_INFO("More activity on right, moving RIGHT.");
            		cmd.states[Y] = ARM_RIGHT;
            	}
                // Currently all axes have the same speed
                cmd.speeds.fill(static_cast<int8_t>(1));

                // Everything else is 0 (doesn't move)
                cmd.states[Z] = 0;
                cmd.states[YAW] = 0;
                cmd.states[PITCH] = 0;
                cmd.states[ROLL] = 0;
                cmd.states[GRIP] = 0;
                cmd.states[LIFT] = 0;
            	cmd_pub_.publish(cmd);

                x = 0;

        	}
        	else
        	{
        		ROS_INFO("Sides of dish not different enough to trigger movement.");
        	}
        }
        

    }

}

void ActVector::init()
{
	// Initialize the publisher
    //     Cartesian commands or constant move commands: for now you can use one
    //     or the other. Keep one commented out.
    //cmd_pub_ = n_.advertise<arm::cartesian_moves>("cartesian_moves", 1000);
    cmd_pub_ = n_.advertise<arm::constant_move>("constant_moves", 1);

    

    ROS_INFO("Waiting for subscribers...");
    while((cmd_pub_.getNumSubscribers() < 1) && ros::ok());
    ROS_INFO("Activation Vector controller got a subscriber.");

	// Initialize the subscriber
	dish_state_sub_ = n_.subscribe("dish_states_to_burst_creator", 1000, &ActVector::callback, this);

	// Initialize the BufferSpikeDetector
	int buffer_size_ = 3000;
	double stdev_mult_ = 2.0;
	buf_.init(buffer_size_, stdev_mult_);

	// Zero the arrays
	frameCounter = 0;
	for(int ii = 0; ii < 60; ii++)
	{
		lastFrame[ii] = 0;
		activation_[ii] = 0;
	}

    
	
    lastSent = ros::Time::now();
	run();
}


int main(int argc, char** argv)
{
	ros::init(argc, argv, "act_vector");

	//Creator calls init(), which calls run()
	ActVector av;
    
	return 0;

}
