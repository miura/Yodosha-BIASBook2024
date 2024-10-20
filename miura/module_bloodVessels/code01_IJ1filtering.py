from ij import ImagePlus
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

ClosingRadius = 6  	# (um)
Nthreads = 2		# (3D filter multi-threading)

orgimp = ImagePlus("/Users/miura/samples/BloodVessels_small.tif")
fastfiltered_imp = fast3Dclose(orgimp, ClosingRadius, Nthreads)
fastfiltered_imp.show()





