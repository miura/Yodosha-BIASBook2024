from ij import ImagePlus, IJ
from ij.process import ImageConverter
from ij.process import StackStatistics
from fiji.threshold import Auto_Threshold

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

tubeimp = ImagePlus("/Users/miura/samples/BloodVessels_small_tubed.tif") 
tube8bimp = convertTo8bit(tubeimp)
tube8bimp.setTitle("BloodVessels_small_tubed8b.tif")
tube8bimp.show()
binimp = getThresholdedImage( tube8bimp )
binimp.setTitle("BloodVessels_small_binary.tif")
binimp.show()


