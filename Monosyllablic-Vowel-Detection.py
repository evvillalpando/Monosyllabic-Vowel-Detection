modulePath = 'C:/Users/Eddie/Desktop/src/'
import sys
sys.path.append(modulePath)
import myWave
import dspUtil
from numpy import median
import generalUtility
import praatUtil
from matplotlib import pyplot as plt
import matplotlibUtil
 
# recognizing syllable nuclei using intensity or f0
# use interval of recognized nuclei for text grid annotation
 
path = 'C:/Users/Eddie/Desktop/src/'
path2 = 'C:/Users/Eddie/Documents/Python Scripts/'
suffix = 'wav'
fName = 'C:/Users/Eddie/Desktop/src/shit.wav'
 
##Normalize audio file##
numChannels, numFrames, fs, data = myWave.readWaveFile(fName)
data[0] = dspUtil.normalize(data[0])
n = len(data[0])
duration = float(n) /float(fs)
fileNameOnly = generalUtility.getFileNameOnly(fName)
outputFileName = fileNameOnly + "processed.wav"
myWave.writeWaveFile(data, outputFileName, fs, True)
 
#Calculate & Read F0 to exclude unvoiced segments#
praatUtil.calculateF0(path2 + outputFileName)
pitches = path2 + fileNameOnly + 'processed.PitchTier'
pitchT, pitchV = praatUtil.readPitchTier(pitches)
pitchT = list(pitchT)
 
 
##Graph DBxTime, i.e. intensity graph##
dataT, dataI = praatUtil.calculateIntensity(path2 + outputFileName)
graph = matplotlibUtil.CGraph(width = 8, height = 3)
graph.createFigure()
ax = graph.getArrAx()[0]
ax.plot(dataT, dataI, linewidth = 2)
ax.set_xlabel("Time [s]")
ax.set_ylabel("SPL [dB]")
ax.set_title(fileNameOnly)
graph.padding = 0.1
graph.adjustPadding(bottom = 2, right = 0.5)
ax.grid()
matplotlibUtil.setLimit(ax, dataI, 'y', rangeMultiplier = 0.1)
matplotlibUtil.formatAxisTicks(ax, 'y', 6, '%d')
plt.savefig(fileNameOnly + "_intensity.png")
dataI = list(dataI)
dataT = list(dataT)
 
##Median dB value of file calculated. values +2 over median are added to a list; first and second values determined start and end of vowel##
shitList = []
for x in dataI:
    if x>(median(dataI) + 2):
         shitList.append(x)
firstvalue = shitList[0]
secondvalue = shitList[-1]
startTime = 0
for x in range(0,len(dataT)):
    if dataI[x] > firstvalue and startTime == 0 and dataT[x]>=pitchT[0]:
        print dataT[x], dataI[x], pitchT[0]
        startTime = dataT[x]
    elif startTime == 0:
        continue
    if dataI[x] < secondvalue and dataT[x]<=pitchT[-1]:
        endTime = dataT[x]
        break
#for x in dataT:
#    if x<pitchT[0]:
#        shitList
##Make textgrid with calculated startTime and endTime of vowel##
def mkTextGrid(filestart,fileend,intervalName,intervalstart,intervalend,filename):
    f = open(path + filename, 'w')
    f.write('File type = "ooTextFile"\n')
    f.write('Object class = "TextGrid"\n')
    f.write('\n')
    f.write('xmin = ' + str(filestart) + ' \n')
    f.write('xmax = ' + str(fileend) + ' \n')
    f.write('tiers? <exists> \n')
    f.write('size = ' + str(1) + ' \n')
    f.write('item []: \n')
    f.write('    item [1]:\n')
    f.write('        class = "IntervalTier" \n')
    f.write('        name = "' + intervalName + '" \n')
    f.write('        xmin = ' + str(intervalstart) + ' \n')
    f.write('        xmax = ' + str(intervalend) + ' \n')
    f.write('        intervals: size = 1 \n')
    f.write('        intervals [' + str(1) + ']:\n')
    f.write('            xmin = ' + str(intervalstart) + '\n')
    f.write('            xmax = ' + str(intervalend) + '\n')
    f.write('            text = \"\"\n')
    f.close()
mkTextGrid(0,duration,'vowel',startTime,endTime,'shitprocessed.TextGrid')
