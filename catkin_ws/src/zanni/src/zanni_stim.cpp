#include "ros/ros.h"
#include <comedilib.h>
#include "zanni/Stim.h"

comedi_t *daq_dev;
int analogOut;
int aref = AREF_GROUND;

void print_cmd(comedi_cmd cmd) {
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

	ROS_WARN("channel count: %u\n", cmd.chanlist_len);
}

//From http://www.ib.cnea.gov.ar/~servos/Comedi/html/x403.html
int comedi_internal_trigger(comedi_t *dev, unsigned int subd,
		unsigned int trignum) {
	comedi_insn insn;
	lsampl_t data[1];

	memset(&insn, 0, sizeof(comedi_insn));
	insn.insn = INSN_INTTRIG;
	insn.subdev = subd;
	insn.data = data;
	insn.n = 1;

	data[0] = trignum;

	return comedi_do_insn(dev, &insn);
}

bool doStim(zanni::Stim::Request &req, zanni::Stim::Response &res) {

	//get the Analog out subdevice
	analogOut = comedi_find_subdevice_by_type(daq_dev, COMEDI_SUBD_AO, 0);

	//Prepare a channel list consisting of the one specified channel
	unsigned int chanlist[1];

	int range = comedi_find_range(daq_dev, analogOut, req.channel, UNIT_volt,
			-8.0, 8.0);
	if (range < 0) {
		ROS_WARN("Couldn't find good output range, using default");
		range = 0;
	}
	ROS_INFO("Stimulating on channel %u", req.channel);
	comedi_range * outRange = comedi_get_range(daq_dev, analogOut, req.channel,
			range);
	lsampl_t maxData = comedi_get_maxdata(daq_dev, analogOut, req.channel);

	//Convert the data from double volts to COMEDI samples
	sampl_t comediSignal[req.signal.size()];
	for (std::vector<double>::size_type ii = 0; ii != req.signal.size(); ++ii) {
		sampl_t comediValue = comedi_from_phys(req.signal[ii], outRange, maxData);
		//ROS_WARN("converting %f to %u", req.signal[ii], comediValue);
		comediSignal[ii] = comediValue;
	}

	//Create a channel list
	chanlist[0] = CR_PACK(req.channel, range, aref);
	int chanlistlen = 1;

	//Set up a comedi command to send data on analog out
	comedi_cmd stim_cmd;
	memset(&stim_cmd, 0, sizeof(stim_cmd));

	stim_cmd.subdev = analogOut;
	stim_cmd.flags = CMDF_WRITE;

	stim_cmd.start_src = TRIG_INT; //On an internal trigger
	stim_cmd.start_arg = 0; //Trigger on trigger 0

	stim_cmd.scan_begin_src = TRIG_TIMER; //Trigger on a timer
	stim_cmd.scan_begin_arg = 1000000; //Put the data back out at the frequency it was acquired at

	stim_cmd.convert_src = TRIG_NOW; //Convert immediately
	stim_cmd.convert_arg = 0; //No time

	stim_cmd.scan_end_src = TRIG_COUNT;
	stim_cmd.scan_end_arg = 1; //Normally the size of the channel list

	stim_cmd.stop_src = TRIG_COUNT; //Stop after a number of scans
	stim_cmd.stop_arg = req.signal.size(); //The number of scans to stop after

	stim_cmd.chanlist = chanlist;
	stim_cmd.chanlist_len = chanlistlen;

	//stim_cmd.data = comediSignal;
	//stim_cmd.data_len = req.signal.size();

	//Test the command
	int retval = comedi_command_test(daq_dev, &stim_cmd);
	switch (retval) {
	case 0:
		ROS_INFO("COMEDI command OK");
		break;
	case 1:
		ROS_WARN("Unsupported trigger removed from COMEDI command");
		print_cmd(stim_cmd);
		break;
	case 2:
		ROS_WARN("Invalid combination of ...src settings in COMEDI command");
		print_cmd(stim_cmd);
		break;
	case 3:
		ROS_WARN("Argument changed to valid range in COMEDI command");
		print_cmd(stim_cmd);
		break;
	case 4:
		ROS_WARN("Argument adjusted in COMEDI command");
		print_cmd(stim_cmd);
		break;
	case 5:
		ROS_WARN("Chanlist in COMEDI command unsupported by board");
		break;
	default:
		break;
	}
	retval = comedi_command_test(daq_dev, &stim_cmd);
	if (retval > 0) {
		ROS_ERROR("COMEDI command could not be corrected");
		ros::shutdown();
	}

	//Send the command
	retval = comedi_command(daq_dev, &stim_cmd);
	if (retval < 0) {
		ROS_ERROR("Failure running COMEDI command: %u: %s", comedi_errno(),
				comedi_strerror(comedi_errno()));
		ros::shutdown();
	}

	//Fill the buffer
	retval = write(comedi_fileno(daq_dev), (void *) comediSignal,
			req.signal.size() * sizeof(sampl_t));
	if (retval < 0) {
		ROS_ERROR("Failure writing data: %u: %s", comedi_errno(),
				comedi_strerror(comedi_errno()));
		ros::shutdown();
	} else {
		ROS_WARN("Wrote %u of %lu bytes", retval,
				req.signal.size() * sizeof(sampl_t));
	}

	//Fire the trigger
	retval = comedi_internal_trigger(daq_dev, analogOut, 0);
	if (retval < 0) {
		ROS_ERROR("Couldn't fire trigger: %u: %s", comedi_errno(),
				comedi_strerror(comedi_errno()));
		ros::shutdown();
	}

	//Delay while it runs
	int status = comedi_get_subdevice_flags(daq_dev, analogOut);
	while (status & SDF_RUNNING) {
		//printf("Running, flags: %08x\n", status);
		status = comedi_get_subdevice_flags(daq_dev, analogOut);
	}

	//Now cancel the command so that future calls don't hang on it.
	comedi_cancel(daq_dev, analogOut);
	if (retval < 0) {
		ROS_ERROR("Couldn't cancel command: %u: %s", comedi_errno(),
				comedi_strerror(comedi_errno()));
		ros::shutdown();
	}

	//We're done here
	res.done = true;
	return true;
}

int main(int argc, char **argv) {

	//Initialize a ROS service to deliver a stimulation
	ros::init(argc, argv, "zanni_stim_server");
	ros::NodeHandle n;
	ros::ServiceServer service = n.advertiseService("deliver_stim", doStim);

	//We're talking to COMEDI, so initialize the card
	int retval;
	int total = 0;

	daq_dev = comedi_open("/dev/comedi0");
	if (daq_dev == NULL) {
		ROS_ERROR("Failed to open COMEDI device");
		ros::shutdown();
	}

	ros::spin();

	return 0;
}
