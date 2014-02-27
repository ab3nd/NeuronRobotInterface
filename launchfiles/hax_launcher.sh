#Launch the recorder
roslaunch ./record.launch &

#Wait 50 seconds
echo "sleeping..."
sleep 50s
echo "starting CSV configuration"

#Launch CSV reader using recorded csv file
roslaunch ./launch_hax.launch



