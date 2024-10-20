from ij import IJ, ImagePlus

imp = ImagePlus( "/Users/miura/bat-cochlea-volume.tif" )
frames = imp.getStackSize()
for i in range(frames):
	ip = imp.getStack().getProcessor(i + 1)
	stats = ip.getStats()
	print("Mean: %.1f slice: %i") % (stats.mean, i+1)