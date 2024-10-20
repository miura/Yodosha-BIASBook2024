from ij import ImagePlus
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

useCalibration = True
sigma = 8 # in the phyisical units

orgimp = ImagePlus("/Users/miura/samples/BloodVessels_small.tif")
tubeimp = tubenessFilter(orgimp, sigma, useCalibration)
tubeimp.show()