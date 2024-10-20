#@ IOService io
#@ OpService ops
#@ UIService ui

def tubeness(img, sigma, cal):
	if sigma < min(cal):
		sigma = min(cal)
	return ops.filter().tubeness(img, sigma, cal)

img = io.open('/Users/miura/samples/BloodVessels_small.tif')

sigma = 8
cal = [img.averageScale(0), img.averageScale(1), img.averageScale(2)]
tubeimg = tubeness(img, sigma, cal)
ui.show(tubeimg)