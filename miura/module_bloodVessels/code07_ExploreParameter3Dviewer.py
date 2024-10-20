from ij import IJ, ImagePlus, ImageStack
from ij3d import Image3DUniverse
from org.scijava.vecmath import Color3f
from java.awt import Color
import jarray

imp = ImagePlus('/Users/miura/samples/BloodVessels_small_tubed8b.tif')
univ = Image3DUniverse()
univ.show()

color = Color3f(Color.WHITE)
obj_name = "vessels"
channels = [True, True, True]
resamplingF = 1
thresholdRange = range(2, 21, 2)
snapsA = []

for threshold in thresholdRange:
	c = univ.addMesh( imp, color, obj_name, threshold, channels, resamplingF)
	snap = univ.takeSnapshot()
	snapsA.append(snap)
	univ.removeAllContents()

univ.close()
jsnapsA = jarray.array(snapsA, ImagePlus)
stack = ImageStack.create(jsnapsA)
outimp = ImagePlus("Thresholding", stack)

for i, th in enumerate(thresholdRange):
	label = "Threshold=" + str(th)
	outimp.getStack().setSliceLabel(label, i + 1)
	
outimp.show()


 


