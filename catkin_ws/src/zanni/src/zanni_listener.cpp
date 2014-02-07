/*
 * zanni_listener.cpp
 *
 *  Created on: Sep 26, 2013
 *      Author: ams
 */


#include "ros/ros.h"
#include "zanni/Channels.h"
#include <ncurses.h>

#define GSIZE 8
#define CSV

using namespace std;

void chatterCallback(const zanni::Channels::ConstPtr& msg)
{
#ifdef CSV
	//CSV formatted output on stdout
	cout << msg->voltages[0];
	for(int ii = 1; ii < 64; ii++)
	{
		if ((ii == 0)||(ii == 7)||(ii == 56)||(ii == 63))
		{
			continue;
		}
		cout << "," << msg->voltages[ii];

	}
	cout << endl;

#else
	for(int ii = 0; ii < 8; ii++){
  	for(int jj = 0; jj < 8; jj++)
  	{
  		int index = (ii * GSIZE) + jj;
  		//ROS_WARN("%u", index);
  		mvprintw(jj * 3, ii * 9, "%#8.6g ", msg->voltages[index]);
  	}
  }
  refresh();
#endif
}

int main(int argc, char **argv)
{

  //Setup for ncurses
  initscr();
  noecho();

	ros::init(argc, argv, "listener");
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("zanni", 1000, chatterCallback);

  ros::spin();

  //tear down ncurses
  endwin();
  return 0;
}

