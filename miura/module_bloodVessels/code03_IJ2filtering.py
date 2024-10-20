#@ IOService io
#@ OpService ops
#@ UIService ui

from net.imglib2.type.numeric.integer import UnsignedByteType
#from net.imglib2.algorithm.neighborhood import DiamondShape
from net.imglib2.algorithm.neighborhood import HyperSphereShape

def ops_morphClose(img, ClosingRadius):
	radx = long( ClosingRadius / img.averageScale(0))
	shape = HyperSphereShape( radx )
	result = ops.create().img( img, UnsignedByteType())
	ops.morphology().close( result, img, [ shape ]  )
	return result
	
ClosingRadius = 6  	# (um)

bspath = "/Users/miura/samples/BloodVessels_small.tif"
img = io.open(bspath)
ui.show(img)
result = ops_morphClose(img, ClosingRadius)
ui.show( result )
