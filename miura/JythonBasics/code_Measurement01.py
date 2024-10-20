from ij import IJ, ImagePlus

imp = ImagePlus( "/Users/miura/bat-cochlea-volume.tif" )
frames = imp.getStackSize()
IJ.run("Set Measurements...", " mean slice redirect=None decimal=3")
IJ.run("Clear Results")
for i in range(frames):
	imp.setSlice(i + 1)
	imp.updateImage()
	IJ.run("Measure")
