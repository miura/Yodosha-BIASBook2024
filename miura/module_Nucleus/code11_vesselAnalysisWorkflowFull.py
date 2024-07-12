from ij import ImagePlus, IJ
from ij.plugin import LutLoader
from ij.process import LUT
from ij.process import ImageConverter
from ij.process import StackStatistics
from fiji.threshold import Auto_Threshold
from mcib3d.image3d.processing import FastFilters3D
from features import TubenessProcessor
from sc.fiji.skeletonize3D import Skeletonize3D_
from sc.fiji.analyzeSkeleton import AnalyzeSkeleton_
from inra.ijpb.binary import BinaryImages
from inra.ijpb.label.select import LabelSizeFiltering
from inra.ijpb.label.select import RelationalOperator
from inra.ijpb.binary.distmap import ChamferMask3D
from inra.ijpb.label.filter import ChamferLabelDilation3DShort
import  Replace_Value
from ij3d import Image3DUniverse


# MCIB3D 
def fast3Dclose(orgimp, ClosingRadius, Nthreads):
	radx = ClosingRadius / cal.pixelWidth
	rady =  ClosingRadius / cal.pixelHeight
	radz =  ClosingRadius / cal.pixelDepth
	
	res = FastFilters3D.filterIntImageStack(\
		orgimp.getStack(), FastFilters3D.CLOSEGRAY, \
		radx, rady, radz, Nthreads, True)
	fastfiltered_imp = ImagePlus("filtered", res)
	fastfiltered_imp.setCalibration(cal)
	return fastfiltered_imp

def tubenessFilter(filteredimp, sigma, useCalibration):
	# check if sigma is larger than the resolution
	minimumSeparation = min(cal.pixelWidth, cal.pixelHeight, cal.pixelDepth)
	if sigma < minimumSeparation:
		sigma = minimumSeparation
 
	tp = TubenessProcessor(useCalibration)
	tp.setSigma(sigma)
	result = tp.generateImage(filteredimp)
	result.setCalibration(cal)
	return result


# Convert 32-bit image to 8-bit without clipping
def convertTo8bit(tubeimp):
	tube8bimp =  tubeimp.duplicate()
	sstats = StackStatistics(tube8bimp)
	smax = sstats.max
	smin = sstats.min
	IJ.setMinAndMax(tube8bimp, smin, smax)
	ic = ImageConverter(tube8bimp)
	ic.convertToGray8()
	return tube8bimp

# Defaul value: 8
def getThresholdedImage( tube8bimp ):
	binimp = tube8bimp.duplicate()
	sstats = StackStatistics( binimp )
	hist = sstats.histogram()
	histint = map(int, hist)
	lowTH = Auto_Threshold.Huang(histint)
	print("Lower threshold: " + str(lowTH))
	
	for i in range(binimp.getStackSize()):
		binimp.getStack().getProcessor( i + 1 ).threshold(lowTH)
    
	return binimp

def filterLabelTubes(binimp, sizeLimit):
	labeledimp = BinaryImages.componentsLabeling\
		(binimp, connectivity, bitdepth)
	gilut = LutLoader.getLut("glasbey_inverted")
	labeledimp.setLut(gilut)
	sizeFilter = LabelSizeFiltering\
		(RelationalOperator.GT, sizeLimit)
	filteredlabeledimp = sizeFilter.process(labeledimp)
	filteredlabeledimp.setCalibration(cal)
	return filteredlabeledimp

def skeletonize3D( filteredlabeledimp ):
	skelimp = filteredlabeledimp.duplicate()
	skz = Skeletonize3D_()
	skz.setup("", skelimp)
	skz.run(None)
	return skelimp


### execution starts from here
orgimp = ImagePlus("/Users/miura/samples/BloodVessels_small.tif")

cal = orgimp.getCalibration()
	
ClosingRadius = 6  	# (um) 3D filter
Nthreads = 2		# (multi-threading) 3D filter
fastfiltered_imp = fast3Dclose(orgimp, ClosingRadius, Nthreads)
fastfiltered_imp.show()

useCalibration = True # Tubuness filtering 
sigma = 8 # (um) Tubuness filtering

tubeimp = tubenessFilter(fastfiltered_imp, sigma, useCalibration)
tubeimp.show() 

#tubeimp = ImagePlus("/Users/miura/samples/BloodVessels_small_tubed.tif") 
tube8bimp = convertTo8bit(tubeimp)
tube8bimp.setTitle("BloodVessels_small_tubed8b.tif")
tube8bimp.show()
binimp = getThresholdedImage( tube8bimp )
binimp.setTitle("BloodVessels_small_binary.tif")
binimp.show()

connectivity = 26
bitdepth = 8 	# bitdepth of the label image
sizeLimit = 1000 #size filtering threshold
filteredlabeledimp = filterLabelTubes(binimp, sizeLimit)
filteredlabeledimp.setTitle("BloodVessels_small_label.tif")
filteredlabeledimp.show()

skelimp = skeletonize3D( filteredlabeledimp )
skelimp.setTitle("BloodVessels_small_Skel.tif")
skelimp.show()



def analyzeSkeleton3D( skelimp ):
	skel = AnalyzeSkeleton_()
	skel.setup("", skelimp)
	pruneIndex = AnalyzeSkeleton_.NONE
	pruneEnds = False
	shortPath = False
	origImp = None
	silent = True
	verbose = False
	skelResult = skel.run(pruneIndex, \\
		pruneEnds, shortPath, origImp, silent, verbose)
	return skel, skelResult
	
# standard deviation
def sd( l ):
	mean = float(sum(l))/len(l)
	ss = sum((x-mean)**2 for x in l)
	sd = (ss/(len(l)-1))**0.5
	return sd
#tortuosity
def calcTortuosity(edge):
	length = edge.getLength()
	v1p = edge.getV1().getPoints().get(0)
	v2p = edge.getV2().getPoints().get(0)
	dist = skel.calculateDistance(v1p, v2p)
	tortuosity = length/dist
	return tortuosity
	
#skelimp = ImagePlus(\\
#	"/Users/miura/samples/BloodVessels_small_skel.tif")
#cal = skelimp.getCalibration()

skel, skelResult = analyzeSkeleton3D( skelimp )
skeletons = skelResult.getGraph()
juncNums = skelResult.getJunctions()
### stats ###
imWidth = skelimp.getWidth() * cal.pixelWidth
imHeight = skelimp.getHeight() * cal.pixelHeight
imDepth = skelimp.getNSlices() * cal.pixelDepth
totalVolume = imWidth * imHeight * imDepth #um^3
totalVolume = totalVolume / pow(1000, 3) #mm^3

Alltortuosity = []
AllBranchLen = []
for s in skeletons:
	edgeList = s.getEdges()
	tortuosityA = map(calcTortuosity, edgeList)
	Alltortuosity += tortuosityA
	branchLengthA = map(\\
		lambda e:e.getLength(), edgeList)
	AllBranchLen += branchLengthA

totalBranchlens = sum(AllBranchLen)
totalBranchNum = len(AllBranchLen)
ave_BranchLen = totalBranchlens / totalBranchNum
sd_BranchLen = sd(AllBranchLen)
branchDensity = totalBranchNum / totalVolume
vesselLengthDensity = totalBranchlens / totalVolume
totaljuncs = sum(juncNums)
junctionDensity = totaljuncs / totalVolume
ave_tortuosity = sum(Alltortuosity) / len(Alltortuosity)

print("Image Width: " + str(imWidth) +  " (um)")
print("Total Imaged Volume: " + \\
	str(totalVolume) + " (mm^3)")
print("Total Branch Length: " + \\
	str(totalBranchlens) + " (um)")
print("Total Branch Number: " + \\
	str(totalBranchNum))
print("Average Branch Length: " + \\
	str(ave_BranchLen) + " (um)")
print("... standard deviation: " + \\
	str(sd_BranchLen) + " (um)")
print("Branch Density: " + \\
	str(branchDensity) + " (/mm^3)")
print("Vessel Length Density: " + \\
	str(vesselLengthDensity/1000) + \\
		" (mm/mm^3)")
print("Total Junction Number: " + \\
	str(totaljuncs))
print("Junction Density: " + \\
	str(junctionDensity) + " (/mm^3)")
print("Average Tortuosity: " + str(ave_tortuosity))

### visalization

# tagged image visualization
tagstack = skel.getResultImage(False)
tagimp = ImagePlus("tagged", tagstack)

rv = Replace_Value()
rv.setup(None, tagimp)
rv.doit(70, 215)
rv.doit(30, 250)

radius = 1.0
algo = ChamferLabelDilation3DShort(\\
	ChamferMask3D.SVENSSON_3_4_5_7, radius)
tagstackDilated = algo.process(tagstack)
tagDilatedimp = ImagePlus("tagDilated", tagstackDilated)

fireLL = LutLoader.getLut("fire")
fireLut = LUT(fireLL, float(0), float(255))
tagDilatedimp.setLut(fireLut)

univ = Image3DUniverse()
c = univ.addVoltex(tagDilatedimp)
univ.show()

# labeled image visualization
labelstack = skel.getLabeledSkeletons()
labelstack = algo.process(labelstack)
labelimp = ImagePlus("labeled", labelstack)
currentState = ImageConverter.getDoScaling()
ImageConverter.setDoScaling(False)
ImageConverter(labelimp).convertToGray8()
ImageConverter.setDoScaling(currentState)

giLut = LutLoader.getLut("Glasbey on Dark")
labelimp.setLut(giLut)

univ2 = Image3DUniverse()
c2 = univ2.addVoltex(labelimp)
univ2.show()


