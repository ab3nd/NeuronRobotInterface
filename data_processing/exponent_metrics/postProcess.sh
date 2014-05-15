#!/bin/sh
python ./gather_values.py
# --== Bicuculline experiment ==--
#Mature cultures with bicuculline
cat scaleExps.csv | grep "control bicuculline" > control-bicuculline-scale.csv
cat spikeRates.csv | grep "control bicuculline" > control-bicuculline-spike.csv
#Control developing cultures
cat scaleExps.csv | grep "controlepilepsy bicuculline" > control-epilepsy-bicuculline-scale.csv
cat spikeRates.csv | grep "controlepilepsy bicuculline" > control-epilepsy-bicuculline-spike.csv
#Developing cultures that got bicuculline after epileptic phase
cat scaleExps.csv | grep "post-epilepsy bicuculline" > post-epilepsy-bicuculline-scale.csv
cat spikeRates.csv | grep "post-epilepsy bicuculline" > post-epilepsy-bicuculline-spike.csv
#Developing cultures that got bicuculline before initial epileptic phase and kept getting it after
cat scaleExps.csv | grep "pre-epilepsy bicuculline" > pre-epilepsy-bicuculline-scale.csv
cat spikeRates.csv | grep "pre-epilepsy bicuculline" > pre-epilepsy-bicuculline-spike.csv

# --== Stimulation Experiment ==--
#Continuous stimulation
cat scaleExps.csv | grep "continuous " > continuious-stim-scale.csv
cat spikeRates.csv | grep "continuous " > continuious-stim-spike.csv
#Single stimulation
cat scaleExps.csv | grep "single stim" > single-stim-scale.csv
cat scaleExps.csv | grep "singlestim" >> single-stim-scale.csv
cat spikeRates.csv | grep "single stim" > single-stim-spike.csv
cat spikeRates.csv | grep "singlestim" >> single-stim-spike.csv
#Mature cultures, unstimulated
cat scaleExps.csv | grep "control 1" > no-stim-scale.csv
cat scaleExps.csv | grep "control 2" >> no-stim-scale.csv
cat scaleExps.csv | grep "control 3" >> no-stim-scale.csv
cat spikeRates.csv | grep "control 1" > no-stim-spike.csv
cat spikeRates.csv | grep "control 2" >> no-stim-spike.csv
cat spikeRates.csv | grep "control 3" >> no-stim-spike.csv

#My simulated data
cat scaleExps.csv | grep "_labview_" > simulated-scale.csv
cat spikeRates.csv | grep "_labview_" > simulated-spike.csv

