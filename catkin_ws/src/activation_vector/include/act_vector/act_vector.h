
#ifndef ACT_VECTOR_H_
#define ACT_VECTOR_H_

#include "ros/ros.h"
#include "neuro_recv/dish_state.h"
#include "burst_calc/buffer_spike_detector.h"
#include "arm/cartesian_move.h"
#include "arm/cartesian_moves.h"
#include "arm/constant_move.h"
#include "arm/constant_move_time.h"
#include "movement_definitions.h"
#include <vector>
#include <cmath>

class ActVector
{
public:
    ActVector() { init(); }

private:
    void callback(const neuro_recv::dish_state::ConstPtr& d);
    void run();
    void init();
    void processDish(neuro_recv::dish_state d);

    double euclidianDistance(double a[], double b[]);

    BufferSpikeDetector buf_;

    ros::NodeHandle n_;
    ros::Subscriber dish_state_sub_;
    ros::Publisher cmd_pub_;
    ros::Time lastSent;
    std::vector<neuro_recv::dish_state> dishes_;
    std::vector<neuro_recv::dish_state> dishes_in_process_;

    //IIRC, this is something like a 5 billion year runtime before overflow
    double frameCounter;
    double lastFrame[60];
    double activation_[60];
    double normActivation_[60];

    //Not great with unsplit culture
    //weirdly bursty output with split culture
//    double lAct[60]={
//    		1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
//       1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
//       1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
//       1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       	    0.0, 0.0, 0.0, 0.0, 0.0, 0.0
//    };
//
//    double rAct[60]={
//    		0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
//       1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
//       1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
//       	    1.0, 1.0, 1.0, 1.0, 1.0, 1.0
//    };

    //Looks kind of good with split culture
    double lAct[60]={
    		1.0, 1.0, 0.0, 0.0, 0.0, 0.0,
       1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       	    1.0, 1.0, 0.0, 0.0, 0.0, 0.0
    };

    double rAct[60]={
    		0.0, 0.0, 0.0, 0.0, 1.0, 1.0,
       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
       	    0.0, 0.0, 0.0, 0.0, 1.0, 1.0
    };

    //These were pretty much the same with the split culture
//    double lAct[60]={
//    		0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//            0.0, 0.0, 0.0, 0.0, 0.0, 0.0
//    };
//
//    double rAct[60]={
//    		0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//            0.0, 0.0, 0.0, 0.0, 0.0, 0.0
//    };

    //Rotated version of above, also pretty much the same
//    double lAct[60]={
//    		0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//            0.0, 0.0, 0.0, 0.0, 0.0, 0.0
//    };
//
//    double rAct[60]={
//    		0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0,
//       0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0,
//            0.0, 0.0, 0.0, 0.0, 0.0, 0.0
//    };
    double zeros[60]={
    		0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       	    0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    };

};
#endif
