#include "ros/ros.h"
#include "std_msgs/String.h"

#include <sstream>
#include <comedilib.h>
#include "zanni/Channels.h"

#define CHAN_CNT 64
int analog_in = 0;
int channel = 0;
int range = 0;
int aref = AREF_GROUND;

static unsigned int chanlist[CHAN_CNT];
static comedi_range * range_info[CHAN_CNT];
static lsampl_t maxdata[CHAN_CNT];

//Char buffer for incoming data
#define BUFSZ 10000
char buf[BUFSZ];

// from www.comedi.org/doc/asyncprogram.html
void print_datum(lsampl_t raw, int channel_index) {
	//printf("%u ", raw);
	double physical_value;
	physical_value = comedi_to_phys(raw, range_info[channel_index],
			maxdata[channel_index]);
	printf("%#8.6g ", physical_value);
}

/* from www.comedi.org/doc/asyncprogram.html
 * This prepares a command in a pretty generic way.  We ask the
 * library to create a stock command that supports periodic
 * sampling of data, then modify the parts we want. */
int prepare_cmd_lib(comedi_t *dev, int subdevice, int n_scan, int n_chan,
		unsigned scan_period_nanosec, comedi_cmd *cmd) {
	int ret;

	memset(cmd, 0, sizeof(*cmd));

	/* This comedilib function will get us a generic timed
	 * command for a particular board.  If it returns -1,
	 * that's bad. */
	ret = comedi_get_cmd_generic_timed(dev, subdevice, cmd, n_chan,
			scan_period_nanosec);
	if (ret < 0) {
		printf("comedi_get_cmd_generic_timed failed\n");
		return ret;
	}

	/* Modify parts of the command */
	cmd->chanlist = chanlist;
	cmd->chanlist_len = n_chan;
	if (cmd->stop_src == TRIG_COUNT)
		cmd->stop_arg = n_scan;

	return 0;
}

void print_cmd(comedi_cmd cmd){
	ROS_WARN("subdev: %u\n", cmd.subdev);
	ROS_WARN("flags: %u\n", cmd.flags);

	ROS_WARN("start_src: %u\n", cmd.start_src);
	ROS_WARN("start_arg: %u\n", cmd.start_arg);

	ROS_WARN("scan_begin_src: %u\n", cmd.scan_begin_src);
	ROS_WARN("scan_begin_arg: %u\n", cmd.scan_begin_arg);

	ROS_WARN("convert_src: %u\n", cmd.convert_src);
	ROS_WARN("convert_arg: %u\n", cmd.convert_arg);

	ROS_WARN("scan_end_src: %u\n", cmd.scan_end_src);
	ROS_WARN("scan_end_arg: %u\n", cmd.scan_end_arg);

	ROS_WARN("stop_src: %u\n", cmd.stop_src);
	ROS_WARN("stop_arg: %u\n", cmd.stop_arg);

	ROS_WARN("channel count: %u\n",cmd.chanlist_len);
}


/**
 * This tutorial demonstrates simple sending of messages over the ROS system.
 */
int main(int argc, char **argv) {
	//Initialize ROS, set up the publisher
	ros::init(argc, argv, "zanni_MEA_reader");
	ros::NodeHandle n;
	ros::Publisher zanni_pub = n.advertise<zanni::Channels>("zanni", 1000);
	ros::Rate loop_rate(100);

	//Initialize COMEDI
	//TODO A lot of this should end up as configuration settings
	comedi_t *daq_dev;
	lsampl_t data;
	int retval;
	int total = 0;

	daq_dev = comedi_open("/dev/comedi0");
	if (daq_dev == NULL) {
		ROS_ERROR("Failed to open COMEDI device");
		ros::shutdown();
	}

	int subdev_flags = comedi_get_subdevice_flags(daq_dev, analog_in);

	//prepare a channel list
	for (int ii = 0; ii < CHAN_CNT; ii++) {
		//All get the same range and aref
		chanlist[ii] = CR_PACK(ii, range, aref);
    //MEA-1060 has +/-4mV input, gain of 1200, so output of +/-4.8V
		//range = comedi_find_range(daq_dev, analog_in, channel, UNIT_volt, -4.0, 4.0);
		range = comedi_find_range(daq_dev, analog_in, channel, UNIT_volt, -0.04, 0.04);
		if(range < 0)
		{
			range = 0;
		}
		range_info[ii] = comedi_get_range(daq_dev, analog_in, channel, range);
		maxdata[ii] = comedi_get_maxdata(daq_dev, analog_in, channel);
	}
	ROS_INFO("Using range %u\n", range);

	// Set up a continuous acquisition command.
	comedi_cmd stream_cmd;
	stream_cmd.subdev = analog_in;
	stream_cmd.flags = CR_PACK_FLAGS(channel, range, aref, TRIG_ROUND_NEAREST);

	stream_cmd.start_src = TRIG_NOW; //Start immediately
	stream_cmd.start_arg = 0; //Start in zero nanoseconds (only 0 is supported for TRIG_NOW)

	stream_cmd.scan_begin_src = TRIG_TIMER; //Scan all channels on a timer
	stream_cmd.scan_begin_arg = 1000000; //Time between scans in nanoseconds, 1M is 0.001 seconds or 1Khz

	stream_cmd.convert_src = TRIG_TIMER; //Do the conversions immediately
	stream_cmd.convert_arg = 0; //No delay

	stream_cmd.scan_end_src = TRIG_COUNT; //Done with scan after the channel count is scan_end_arg
	stream_cmd.scan_end_arg = CHAN_CNT; //Scan all 64 channels

	stream_cmd.stop_src = TRIG_NONE; //Don't ever stop acquiring
	stream_cmd.stop_arg = 0; //Don't set this to anything other than 0 ("reserved" according to docs)

	stream_cmd.chanlist = chanlist;
	stream_cmd.chanlist_len = CHAN_CNT;

	retval = comedi_command_test(daq_dev, &stream_cmd);
	switch (retval) {
	case 0:
		ROS_INFO("COMEDI command OK");
		break;
	case 1:
		ROS_WARN("Unsupported trigger removed from COMEDI command");
		print_cmd(stream_cmd);
		break;
	case 2:
		ROS_WARN("Invalid combination of ...src settings in COMEDI command");
		print_cmd(stream_cmd);
		break;
	case 3:
		ROS_WARN("Argument changed to valid range in COMEDI command");
		print_cmd(stream_cmd);
		break;
	case 4:
		ROS_WARN("Argument adjusted in COMEDI command");
		print_cmd(stream_cmd);
		break;
	case 5:
		ROS_WARN("Chanlist in COMEDI command unsupported by board");
		break;
	default:
		break;
	}
	retval = comedi_command_test(daq_dev, &stream_cmd);
	if (retval > 0) {
		ROS_ERROR("COMEDI command could not be corrected");
		ros::shutdown();
	}

	//Launch the command!
	retval = comedi_command(daq_dev, &stream_cmd);
	if (retval < 0) {
		ROS_ERROR("Failure running COMEDI command");
		ros::shutdown();
	}

	double physical_value = 0.0;

	while (ros::ok()) {

		zanni::Channels msg;

		retval = read(comedi_fileno(daq_dev), buf, BUFSZ);
		if (retval < 0) {
			/* some error occurred */
			ROS_ERROR("Read of COMEDI device failed");
			ros::shutdown();
		} else if (retval == 0) {
			//Do nothing? Probably means we are out of data to read
		} else {

			static int col = 0;
			int bytes_per_sample;
			total += retval;

			if (subdev_flags & SDF_LSAMPL)
				bytes_per_sample = sizeof(lsampl_t);
			else
				bytes_per_sample = sizeof(sampl_t);

			for (int ii = 0; ii < retval / bytes_per_sample; ii++) {
				if (subdev_flags & SDF_LSAMPL) {
					data = ((lsampl_t *) buf)[ii];
				} else {
					data = ((sampl_t *) buf)[ii];
				}

				//convert to physical value (volts)
				physical_value = comedi_to_phys(data, range_info[col],	maxdata[col]);
				//ROS_WARN("converting %u to %f", data, physical_value);

				//Put it in a message
				msg.voltages[col] = physical_value;

				col++;
				if (col == CHAN_CNT) {
					zanni_pub.publish(msg);
					col = 0;
				}
			}
		}

		ros::spinOnce();

		loop_rate.sleep();
	}

	return 0;
}
