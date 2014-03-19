'''
Load labview data files and retrieve data from them.

This uses the Decimal class for all data storage because float cannot accurately 
represent numbers like 0.1 (or anything else that isn't a power of 2). This makes for
errors because if you use 0.009 as a key, it actually stores as 0.00899999999999993 
or something like that, and so retrieving the value using 0.009 fails. 

'''

import decimal #Needed to get around problems with decimal representation
import pprint #Mostly for debugging
class LabViewLoader:
    
    def __init__(self):
        self.data = {}
        self.header = {}
        self.rows = {}
        self.cols = {}
        
    def load(self, filename):
        infile = open(filename, 'r')
        line = infile.readline()
        lineElements = line.split('\t')
        #Read the name-value pair header info
        while not lineElements[0] == "***End_of_Header***":
            #print lineElements[0]
            self.header[lineElements[0]] = lineElements[1]
            line = infile.readline()
            lineElements = line.split('\t')
        #Skip the end of header and blank line 
        line = infile.readline()
        line = infile.readline()
        #Get the channel count
        lineElements = line.split('\t')
        self.header[lineElements[0]] = lineElements[1]
        #Read the data header elements
        line = infile.readline()
        lineElements = line.split('\t')
        while not lineElements[0] == "***End_of_Header***":
            self.header[lineElements[0]] = lineElements[1:]
            line = infile.readline()
            lineElements = line.split('\t')
        #Skip the end of header and store the X value column names
        line = infile.readline()
        lineElements = line.split('\t')
        self.header[lineElements[0]] = lineElements[1:]
        #Read the data, store as dictionary of timestamps (column 0) to arrays of data
        line = infile.readline()
        while len(line) > 0:
            #Split on tabs, remove line termination
            line = line.strip()
            values = line.split('\t')
            #Had problems with an empty line at the end of the file getting
            #converted to [''], which has length 1
            if len(values) < 2:
                break
            #Convert to decimal numbers
            #pprint.pprint(values)
            #print "\n"
            self.data[decimal.Decimal(values[0])] = [decimal.Decimal(d) for d in values[1:len(values)]]
            line = infile.readline()
        #Clean up
        #print sorted(self.data.keys())
        infile.close()
          
    '''
    Returns the value at the index if the key exists in the header and has more than 
    one value associated with it or if there is exactly one value associated with it. 
    Returns None if there is no such key in the header or if the index is out of range
    '''
    def getHeaderValue(self, key, index):
        if key in self.header:
            if type(self.header[key]) is str:
                return self.header[key]
            elif len(self.header[key]) > 1 and len(self.header[key]) >= index:
                return self.header[key][index]
            elif len(self.header[key]) == 1:
                return self.header[key]
        return None
    
    '''
    Return the data value at a given key and index, or None if that key or index
    do not exist in the data set
    '''     
    def getDataValue(self, key, index):
        key = decimal.Decimal(key)
        if key in self.data:
            if len(self.data[key]) > 1 and len(self.data[key]) >= index:
                return self.data[key][index]
        return None
    
    def getDataRow(self, key):
        key = decimal.Decimal(key)
        if key in self.data:
            return self.data[key]
        return None
    
    def getAllRows(self):
        rows = []
        step = float(self.getHeaderValue("Delta_X", 1))
        rowCnt = int(self.getHeaderValue("Samples", 1))
        for key in (x * step for x in range (0, rowCnt)):
            key = str(key)
            rows.append(self.getDataRow(key))
        return rows
        
    def getDataCol(self, channel):
        col = None
        if channel in self.cols.keys(): #We saved it earlier and can return it
            col = self.cols[channel]
        else: #We've never been asked about this one, so we have to build it
#             col = []
#             step = float(self.getHeaderValue("Delta_X", channel))
#             rows = int(self.getHeaderValue("Samples", channel))
#             if channel < self.getHeaderValue("Channels", 0):
#                 for key in (x * step for x in range (0, rows)):
#                     key = decimal.Decimal(str(key))
#                     #print key, self.getDataValue(key, channel)
#                     col.append(self.getDataValue(key, channel))
            col = []
            #Get all the keys and sort them. They are timestamps, so this gets them chronologically
            if channel < self.getHeaderValue("Channels", 0):
                for key in sorted(self.data.keys()):
                    col.append(self.getDataValue(key, channel))
                
            #Save it for later, so we don't have to rebuild it
            self.cols[channel] = col
        return col