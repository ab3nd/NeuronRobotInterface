#!/usr/bin/python
import sys

#Split a record.txt file from running the clustering script into two parts:
# 1. NAME_cluster_counts.csv - Counts of clusters based on source LVM file NAME
# 2. NAME_follow_counts.csv - Counts of cluster-follows-other-cluster for source LVM file NAME

#This is effectively a parser for a file called record.txt that has:
#Two lines starting with "Estimated"
#
#Some lines of cluster numbers and cluster counts, of the form "number, count\n"
#   These go into 1 above
#
#A bunch of lines that look like:
# For cluster 166, which occurs 24 times:
#    166 comes after 124 4.0 times, but 124 comes after 166 1 times
#
# For cluster 1, which occurs 69 times:
#    1 comes after 145 4.0 times, but 145 never comes after 1
# These need to get parsed into cluster, count, follows, how many times, percentage, reverse, percentage reverse

# Assume we're called with a full path, at least including the directory
# so call this with something like
# for FILE in `find /media/ams/KINGSTON/ -iname 'record.txt'`; do ./split_records.py $FILE; done
fullpath = sys.argv[1]
stubName = fullpath.split("/")[-2]
countsFile = stubName + "_cluster_counts.csv"
followsFile = stubName + "_follow_counts.csv"

with open(fullpath, 'r') as infile:
    with open(countsFile, 'w') as countsOut:
        countsOut.write("cluster_ID,count\n")
        with open(followsFile, 'w') as followsOut:
            followsOut.write("cluster_ID, count, follows, how_many, percent_follows, reverse_count, percent_reverse\n")
            clusterID = 0
            count = 0
            for line in infile:
                if line.startswith("Estimated"):
                    #ignore it
                    continue
                elif line.startswith("For"):
                    #Get the count from it
                    tokens = line.split()
                    clusterID = tokens[2].split(",")[0]
                    count = tokens[5]
                    #lineOut = ",".join([clusterID, count])
                    #countsOut.write(lineOut)
                    #countsOut.write('\n')
                elif line.startswith("   " + str(clusterID)):
                    tokens = line.split()
                    follows = tokens[3]
                    how_many = tokens[4]
                    reverse_count = 0
                    if tokens[8] == "comes":
                        #There is a reverse
                        reverse = tokens[11]
                    percent_follows = (float(follows)/float(count))*100.0
                    percent_reverse = (float(reverse_count)/float(count))*100.0
                    lineOut = ",".join([clusterID, count, follows, how_many, str(percent_follows), str(reverse_count), str(percent_reverse)])
                    followsOut.write(lineOut)
                    followsOut.write('\n')
                else:
                    values = line.split(",")
                    if len(values) == 2:
                        lineOut = values[0].strip() + "," + values[1].strip()
                        countsOut.write(lineOut)
                        countsOut.write('\n')
            followsOut.close()
        countsOut.close()
    infile.close()