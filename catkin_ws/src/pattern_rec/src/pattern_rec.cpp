//TODO: Some includes
#include "pattern_rec/pattern_rec.h"



//TODO: Write callback function
void PatternRec::dish_recieved()
{

}


void PatternRec::init()
{	
	//dish_state_sub_ = n_.subscribe("dish_states_to_burst_creator", 1000, PatternRec::dish_recieved, this);
}

int main(int argc, char **argv) {
	//ros::init(argc, argv,"pattern_rec");


	//PatternRec pr;

	return 0;
}