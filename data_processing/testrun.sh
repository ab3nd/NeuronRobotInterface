#constants
BICUC_PATH="../../data_sets/labview/lvm_files/Bicucculine_Experiment"
STIM_PATH="../../data_sets/labview/lvm_files/Stimulation_Experiment"

#parameters for mean-shift code
SAMPLES=500
SHIFT=400
CHANNEL=12

#Make a directory to collect everything in
COLLECT_DIR=meanShift_$(date +%Y-%m-%d-%H.%M.%S)
mkdir $COLLECT_DIR

./mean-shift_test.py $BICUC_PATH/control_bicuculline1-13Dec.lvm $SAMPLES $SHIFT $CHANNEL > cluster_counts.csv
mkdir control_bicuc1-13Dec
TOP5=`tail -6 cluster_counts.csv | head -5 | cut -d, -f1`
mkdir top5
for CLUSTER in $TOP5
do
   cp first10-$CLUSTER.png top5/
done
mv top5/ control_bicuc1-13Dec/
mv *.png control_bicuc1-13Dec/
mv cluster_counts.csv control_bicuc1-13Dec/
mv control_bicuc1-13Dec $COLLECT_DIR

./mean-shift_test.py $BICUC_PATH/control_bicuculline3-27Dec.lvm $SAMPLES $SHIFT $CHANNEL > cluster_counts.csv
mkdir control_bicuc3-27Dec
TOP5=`tail -6 cluster_counts.csv | head -5 | cut -d, -f1`
mkdir top5
for CLUSTER in $TOP5
do
   cp first10-$CLUSTER.png top5/
done
mv top5/ control_bicuc3-27Dec/
mv *.png control_bicuc3-27Dec/
mv cluster_counts.csv control_bicuc3-27Dec/
mv control_bicuc3-27Dec $COLLECT_DIR

./mean-shift_test.py $STIM_PATH/22March/22Mar-control_3.lvm $SAMPLES $SHIFT $CHANNEL > cluster_counts.csv
mkdir control3-22Mar
TOP5=`tail -6 cluster_counts.csv | head -5 | cut -d, -f1`
mkdir top5
for CLUSTER in $TOP5
do
   cp first10-$CLUSTER.png top5/
done
mv top5 control3-22Mar/
mv *.png control3-22Mar/
mv cluster_counts.csv control3-22Mar/
mv control3-22Mar $COLLECT_DIR

./mean-shift_test.py $STIM_PATH/22March/22Mar-control_1.lvm $SAMPLES $SHIFT $CHANNEL > cluster_counts.csv
mkdir control1-22Mar
TOP5=`tail -6 cluster_counts.csv | head -5 | cut -d, -f1`
mkdir top5
for CLUSTER in $TOP5
do
   cp first10-$CLUSTER.png top5/
done
mv top5 control1-22Mar/
mv *.png control1-22Mar/
mv cluster_counts.csv control1-22Mar/
mv control1-22Mar $COLLECT_DIR
