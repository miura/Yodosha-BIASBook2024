from ij import ImagePlus, IJ
from ij.process import ImageConverter
from ij.process import StackStatistics
from fiji.threshold import Auto_Threshold
from mcib3d.image3d.processing import FastFilters3D
from features import TubenessProcessor
from inra.ijpb.binary import BinaryImages
from inra.ijpb.label.select import LabelSizeFiltering
from inra.ijpb.label.select import RelationalOperator
from ij.plugin import LutLoader
from sc.fiji.skeletonize3D import Skeletonize3D_

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



