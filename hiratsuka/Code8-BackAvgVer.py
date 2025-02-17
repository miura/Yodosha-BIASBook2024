#baselne estimation

from ij import IJ, ImagePlus
from ij.process import ImageProcessor
from fiji.threshold import Auto_Threshold
from ij.plugin.filter import ThresholdToSelection
from ij.plugin import RoiEnlarger

def estimteBaseLine( imp ):
	# get the middle slice from stack
	sampleslice = imp.getStackSize()
	ip1 = imp.getStack().getProcessor( int(sampleslice/2) ).duplicate()
	# auto threshold value by Triangle algo
	stat1 = ip1.getStats()
	histdouble = stat1.histogram()
	histint = map(lambda x:int(x), histdouble)
	th = Auto_Threshold.Triangle(histint)
	# create selection using the threshold value
	binimp = ImagePlus("Binary", ip1)
	binimp.getProcessor().setThreshold(th, 255, ImageProcessor.NO_LUT_UPDATE)
	boundroi = ThresholdToSelection.run(binimp)
	# enlarge ROI
	boudroiEnlarged = RoiEnlarger.enlarge(boundroi, float(3))
	# invert ROI to select background
	binimp.setRoi(boudroiEnlarged.getInverse(binimp))
	# get the mean intensity of background
	statsbase = binimp.getStatistics()
	baseline = int(round(statsbase.mean))
	print("baseline: " + str(baseline))
	return baseline, binimp

imp = IJ.getImage()
baseline, binimp = estimteBaseLine( imp )
binimp.show()
