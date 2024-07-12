from ij import ImagePlus, IJ
from ij.process import ImageConverter
from ij.process import StackStatistics
from fiji.threshold import Auto_Threshold
from mcib3d.image3d.processing import FastFilters3D


# MCIB3D 
def fast3Dclose(orgimp, ClosingRadius, Nthreads):
	cal = orgimp.getCalibration()
	radx = ClosingRadius / cal.pixelWidth
	rady =  ClosingRadius / cal.pixelHeight
	radz =  ClosingRadius / cal.pixelDepth
	
	res = FastFilters3D.filterIntImageStack(\
		orgimp.getStack(), FastFilters3D.CLOSEGRAY, \
		radx, rady, radz, Nthreads, True)
	fastfiltered_imp = ImagePlus("filtered", res)
	fastfiltered_imp.setCalibration(cal)
	return fastfiltered_imp


from features import TubenessProcessor

def tubenessFilter(filteredimp, sigma, useCalibration):
	cal = filteredimp.getCalibration()
	# check if sigma is larger than the resolution
	minimumSeparation = min(cal.pixelWidth, cal.pixelHeight, cal.pixelDepth)
	if sigma < minimumSeparation:
		sigma = minimumSeparation
 
	tp = TubenessProcessor(useCalibration)
	tp.setSigma(sigma)
	result = tp.generateImage(filteredimp)
	result.setCalibration(cal)
	return result

ClosingRadius = 6  	# (um)
Nthreads = 2		# (3D filter multi-threading)
orgimp = ImagePlus("/Users/miura/samples/BloodVessels_small.tif")
fastfiltered_imp = fast3Dclose(orgimp, ClosingRadius, Nthreads)
fastfiltered_imp.show()

useCalibration = True
sigma = 8 # in the phyisical units

tubeimp = tubenessFilter(fastfiltered_imp, sigma, useCalibration)
tubeimp.show()
