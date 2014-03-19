#Create a LVM header for the given data
#Doesn't properly truncate the header for < 60 channels, but that hasn't been a problem yet

from datetime import datetime

def createHeader(channels, samples, deltaX):
    currentDate = datetime.today()
    dateString = "{0}/{1}/{2}".format(currentDate.year, currentDate.month, currentDate.day)
    fracSeconds = currentDate.second + float(currentDate.microsecond)/1000000
    timeString = "{0}:{1}:{2}".format(currentDate.hour, currentDate.minute, fracSeconds) 
    lvmHeader = '''LabVIEW\tMeasurement    
Writer_Version\t2
Reader_Version\t2
Separator\tTab
Decimal_Separator\t.
Multi_Headings\tYes
X_Columns\tOne
Time_Pref\tAbsolute
Operator\tcsv2lvm.py script
Date\t{0}
Time\t{1}
***End_of_Header***\t    
    
Channels\t{4}
Samples\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}\t{2}
Date\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}\t{0}
Time\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}\t{1}
Y_Unit_Label\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts\tVolts
X_Dimension\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime\tTime
X0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0\t0.0000000000000000E+0
Delta_X\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}\t{3}
***End_of_Header***\t
X_Value\tVoltage_0 (Filtered)\tVoltage_1 (Filtered)\tVoltage_2 (Filtered)\tVoltage_3 (Filtered)\tVoltage_4 (Filtered)\tVoltage_5 (Filtered)\tVoltage_6 (Filtered)\tVoltage_7 (Filtered)\tVoltage_8 (Filtered)\tVoltage_9 (Filtered)\tVoltage_10 (Filtered)\tVoltage_11 (Filtered)\tVoltage_12 (Filtered)\tVoltage_13 (Filtered)\tVoltage_14 (Filtered)\tVoltage_15 (Filtered)\tVoltage_16 (Filtered)\tVoltage_17 (Filtered)\tVoltage_18 (Filtered)\tVoltage_19 (Filtered)\tVoltage_20 (Filtered)\tVoltage_21 (Filtered)\tVoltage_22 (Filtered)\tVoltage_23 (Filtered)\tVoltage_24 (Filtered)\tVoltage_25 (Filtered)\tVoltage_26 (Filtered)\tVoltage_27 (Filtered)\tVoltage_28 (Filtered)\tVoltage_29 (Filtered)\tVoltage_30 (Filtered)\tVoltage_31 (Filtered)\tVoltage_32 (Filtered)\tVoltage_33 (Filtered)\tVoltage_34 (Filtered)\tVoltage_35 (Filtered)\tVoltage_36 (Filtered)\tVoltage_37 (Filtered)\tVoltage_38 (Filtered)\tVoltage_39 (Filtered)\tVoltage_40 (Filtered)\tVoltage_41 (Filtered)\tVoltage_42 (Filtered)\tVoltage_43 (Filtered)\tVoltage_44 (Filtered)\tVoltage_45 (Filtered)\tVoltage_46 (Filtered)\tVoltage_47 (Filtered)\tVoltage_48 (Filtered)\tVoltage_49 (Filtered)\tVoltage_50 (Filtered)\tVoltage_51 (Filtered)\tVoltage_52 (Filtered)\tVoltage_53 (Filtered)\tVoltage_54 (Filtered)\tVoltage_55 (Filtered)\tVoltage_56 (Filtered)\tVoltage_57 (Filtered)\tVoltage_58 (Filtered)\tVoltage_59 (Filtered)\tComment
'''.format(dateString, timeString, samples, deltaX, channels)
    return lvmHeader