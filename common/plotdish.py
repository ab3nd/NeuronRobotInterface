from matplotlib import pyplot as plt

#Plot the data into the file. 
#If you supply less than 60 items of data, it will fail. 
#If you supply more than 60 items of data, they will be ignored. 
def plotdish(data, fileName):
    axisNum = 0
    plt.figure(figsize=(20,12))
    channel = 0
    for row in range(8):
        for col in range(8):
            axisNum += 1
            
            #skip the corners
            if (row == 0) and (col == 0):
                continue
            if (row == 0) and (col == 7):
                continue 
            if (row == 7) and (col == 0):
                continue 
            if (row == 7) and (col == 7):
                continue
           
            ax = plt.subplot(8, 8, axisNum)
            #Get the data from the LVM file
            samples = data[channel]
            channel += 1
            #Convert from Decimal, lose precision, so sad
            samples = [float(str(sample)) for sample in samples]
            plt.plot(samples)
            ax.set_yticklabels([])
            ax.set_xticklabels([])
    plt.tight_layout()
    plt.savefig(fileName + ".png")