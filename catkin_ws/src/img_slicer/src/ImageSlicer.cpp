/*
 * main.cpp
 *
 *  Created on: Jun 26, 2012
 *      Author: ams
 */
#include "ros/ros.h"
#include "sensor_msgs/Image.h"
#include "sensor_msgs/image_encodings.h"
#include "img_slicer/ImageSlicer.h"
#include "cv_bridge/cv_bridge.h"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <stdint.h>
#include <string>
#include <vector>
#include "boost/thread.hpp"

using namespace std;

#define DEBUG
#define WINNAME "Test Window (DEBUG is defined)"

class DataHandler {
private:
	cv_bridge::CvImagePtr cvImgPtr;
	boost::mutex dataUpdate;

public:
	DataHandler() :
			cvImgPtr(new cv_bridge::CvImage) {
	}

	~DataHandler() {
	}

	void messageCallback(sensor_msgs::Image::ConstPtr imgMsg) {
		if (sensor_msgs::image_encodings::isColor(imgMsg->encoding)) {
			//convert to opencv image
			try {
				boost::mutex::scoped_lock lock(dataUpdate);
				cvImgPtr = cv_bridge::toCvCopy(imgMsg,
						sensor_msgs::image_encodings::BGR8);
				//cv::imshow(WINNAME, cvImgPtr->image);

			} catch (cv_bridge::Exception& e) {
				ROS_ERROR("cv_bridge exception converting image: %s", e.what());
				return;
			}
		} else {
			ROS_ERROR("Image Slicer only works on color images");
		}
	}

	vector<uint64> getPixelCounts(uint64 slices) {
		vector<uint64> counts;
		vector<cv::Mat> results(3);
		{
			//scoped lock to avoid update during split
			boost::mutex::scoped_lock lock(dataUpdate);
			try {
				cv::Mat hsvImg;
				//Convert to full range (0-255) HSV
				cv::cvtColor(cvImgPtr->image, hsvImg, CV_BGR2HSV);
				cv::split(hsvImg, results);
				//threshold the image
				cv::Mat hue(((const cv::Mat&) results[0]));
				cv::Mat saturation(((const cv::Mat&) results[1]));
				cv::Mat value(((const cv::Mat&) results[2]));

				cv::threshold((const cv::Mat&) results[0], hue, 165, 65536,
						cv::THRESH_BINARY);

				//Saturation that is too low
				cv::threshold((const cv::Mat&) results[1], saturation, 45,
						65536, cv::THRESH_BINARY);

				//Brightness/value that is too low
				//Turns out I don't need this
				//cv::threshold((const cv::Mat&) results[2], value, 60, 1,cv::THRESH_BINARY_INV);

				//combine all the images
				cv::Mat tmp;
				cv::bitwise_and(hue, saturation, tmp);
#ifdef DEBUG
				cv::imshow(WINNAME, tmp);
#endif

				int count = 0;

				//define the ROI for each section
				//for now, the regions are totally separate
				int regionWidth = tmp.cols / slices;
				for (uint ii = 0; ii < slices; ii++) {
					//ROI corner calculations
					//This should be a rectangle regionWidth wide from the top to bottom of the image
					//This is (x, y, width, height), not two coordinate pairs
					cv::Rect roi((ii * regionWidth), 0, regionWidth, tmp.rows);
					cv::Mat red_roi = tmp(roi);
					//count the pixels in the roi that made it past the threshold
					count = cv::countNonZero(red_roi);
					counts.push_back(count);
					//for now just print it
					//ROS_INFO("Count %i: %i", ii, count);

				}

			} catch (cv::Exception& e) {
				ROS_ERROR("OpenCV error while splitting: %s", e.what());
			}
		}
		return counts;
	}

	bool getSliceCounts(img_slicer::ImageSlicer::Request &sliceCount,
			img_slicer::ImageSlicer::Response &pixCounts) {
		pixCounts.pixelCount = this->getPixelCounts(sliceCount.slices);
		if (pixCounts.pixelCount.size() == 0){
			return false;
		}
		return true;
	}
};

int main(int argc, char** argv) {
	// Set up ROS.
	ros::init(argc, argv, "listener");
	ros::NodeHandle n;

	// Declare variables that can be modified by launch file or command line.
	int rate;
	string topic;

#ifdef DEBUG
	cv::namedWindow(WINNAME, CV_WINDOW_AUTOSIZE);
	cv::startWindowThread();
#endif

	// Initialize node parameters from launch file or command line.
	// Use a private node handle so that multiple instances of the node can be run simultaneously
	// while using different parameters.
	ros::NodeHandle private_node_handle_("~");
	private_node_handle_.param("rate", rate, int(10));
	private_node_handle_.param("topic", topic, string("gscam/image_raw"));

	// Create a handler and have it listen for image messages
	DataHandler *dataHandler = new DataHandler();
	ros::Subscriber sub_message = n.subscribe(topic.c_str(), 100,
			&DataHandler::messageCallback, dataHandler);

	// Tell ROS how fast to run this node.
	ros::Rate r(rate);

	ros::ServiceServer sliceSrv = n.advertiseService("red_px_counts",
			&DataHandler::getSliceCounts, dataHandler);

	//Run in a loop forever
	while (n.ok()) {
		ros::spinOnce();
		r.sleep();
	}

#ifdef DEBUG
	cv::destroyWindow(WINNAME);
#endif
	return 0;
}

