import labviewloader
import argparse
import spike_detector
import ImageDraw, Image
import pprint

if __name__ == '__main__':
    #Get the file name
    ap = argparse.ArgumentParser(description="Load a labview file and characterize the channels by bursts.")
    ap.add_argument('-s', help='Detect spikes instead of bursts', action='store_true')
    ap.add_argument('fname', help='File name to parse')

    args = ap.parse_args()
    
    #Load a labview datafile
    Ll = labviewloader.LabViewLoader()
    print "Loading...",
    Ll.load(args.fname)
    print "done."
    
    #Get a spike detector object
    sd = spike_detector.threshSpikeDetector(threshold = 0.0004)
    
    #get the data column count
    columns = int(Ll.getHeaderValue("Channels", 1))
    samples = int(Ll.getHeaderValue("Samples", 1))
    #Channels to ignore
    ignoreChannels = [56]
    
    #for each column, record where the bursts occur
    burst_record = {}
    for channel in xrange(1, columns-1):
        if channel not in ignoreChannels:
            data = Ll.getDataCol(channel)
            index = 0
            burst_record[channel] = []
            for datum in data:
                index = index + 1
                detect = sd.update(datum)
                if args.s:
                    #Just detecting spikes
                    if detect:
                        burst_record[channel].append(index)
                else:
                    #Detecting bursts
                    if sd.isBursting():
                        burst_record[channel].append(index)
    
    
    #Drop the first 700 samples, as the recording equipment takes time to stabilize
    for channel in burst_record.keys():
        old_entries = burst_record[channel]
        burst_record[channel] = [x for x in old_entries if x > 700]
    
    pprint.pprint(burst_record)   
    
    for l_channel in burst_record.keys():
        first_spike = burst_record[l_channel][0]
        for r_channel in burst_record.keys():
            second_spike = burst_record[r_channel][0]
            if abs(first_spike - second_spike) > 1000:
                diff_seconds = abs(first_spike - second_spike) * float(Ll.getHeaderValue("Delta_X", 1))
                print "Channel {0} spike {1}, Channel {2} spike {3}, Difference:{4}".format(l_channel, first_spike, r_channel, second_spike, diff_seconds)
    #ignores the first 700 samples, as the recording equipment takes time to stabilize
    #
    #for l_canidate in burst_record.keys():
    #    for first_spike in burst_record[l_canidate]:
    #        if first_spike > 700:
    #            for r_canidate in burst_record.keys():
    #                for second_spike in burst_record[r_canidate]:
    #                    if second_spike > 700:
    #                        if first_spike - second_spike < 5000:
    #                            break
    #                        else:
    #                            print "Left channel {0} sample {1}, Right channel {2} sample {3} difference {4}".format(l_canidate, first_spike, r_canidate, second_spike, first_spike-second_spike)
                     
                
    
    #Create a new image measuring 4*channels by 2*samples wide
    mark_width = 2
    mark_height = 2
    image_width = mark_width * samples
    image_height = mark_height * columns
    
    spike_graph = Image.new("RGB", (image_width, image_height))
    drawer = ImageDraw.Draw(spike_graph)
    for channel in xrange(1, columns-1):
        if channel in burst_record.keys():
            for spike in burst_record[channel]:
                right = channel * mark_height
                top = spike * mark_width
                color = "hsl({0}, 100%, 50%)".format(channel * 360/columns)
                drawer.rectangle([(top, right),(top + mark_height, right + mark_width)], outline=color, fill=color)
    spike_graph.save("test_spike_graph", "PNG") 
        
    