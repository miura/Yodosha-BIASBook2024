#code17: extract individual nuclei
from ij import Prefs
from java.awt import Color
from java.awt.image import ColorModel
from ij import IJ, ImagePlus
from ij.gui import Roi
from ij.process import StackStatistics
from ij.plugin import Duplicator
from ij.plugin import ChannelSplitter
from ij.plugin import CompositeConverter
from ij.plugin import ZProjector
from ij.plugin.filter import GaussianBlur
from ij.plugin.filter import Binary
from ij.plugin.filter import ThresholdToSelection
from fiji.threshold import Auto_Threshold
from inra.ijpb.label import LabelImages
from inra.ijpb.binary import BinaryImages
from ij.plugin import LutLoader
from inra.ijpb.plugins import RemoveBorderLabelsPlugin
from inra.ijpb.label.select import LabelSizeFiltering
from inra.ijpb.label.select import RelationalOperator

Prefs.blackBackground = True

def gaussianBlurStack( imp ):
	radius = 2.0
	accuracy = 0.01
	for i in range(imp.getStackSize()):
		GaussianBlur().blurGaussian( \
		   imp.getStack().getProcessor(i+1), \
		   radius, radius, accuracy)

# get Moment threshold value
def thresholdMomentStack( imp ):
	hist = imp.getProcessor().getHistogram()
	lowTH = Auto_Threshold.Moments(hist)
	print "Moment Threshold:", lowTH
	binner = Binary()
	binner.setup("fill", None)	
	# create nucleus mask
	for i in range(imp.getStackSize()):
		ip = imp.getStack().getProcessor(i+1)
		ip.threshold(lowTH)
		binner.run( ip )

# connected component analysis
def connectedComponentAnalysis3D( imp ):	           
	connectivity = 6
	bitdepth = 8
	implabeled = BinaryImages.componentsLabeling\
		(imp, connectivity, bitdepth)
	gilut = LutLoader.getLut("glasbey_inverted")
	implabeled.setLut(gilut)
	return implabeled

#implabeled.show()

# size filtering
def removeSmallOnes(implabeled, sizeLimit):
	sizeFilter = LabelSizeFiltering\
		(RelationalOperator.GT, sizeLimit)
	implabeledFiltered = sizeFilter.process(implabeled)
	return implabeledFiltered

# remove border nucs
def removeBorderNucs( implabeledFiltered ):
	removeLeft = True
	removeRight = True
	removeTop = True
	removeBottom = True
	removeFront = False
	removeBack = False
	implabeledFiltered2 = \
	   RemoveBorderLabelsPlugin.remove(\
	   implabeledFiltered, removeLeft, \
	   removeRight, removeTop, removeBottom, \
	   removeFront, removeBack)
	return implabeledFiltered2

def maxZprojection(stackimp):
	zp = ZProjector(stackimp)
	zp.setMethod(ZProjector.MAX_METHOD)
	zp.doProjection()
	zpimp = zp.getProjection()
	return zpimp

def getBoundingRoi( implabel, nucID):
	offset = 10
	labels = [nucID]
	impOneNuc = LabelImages.keepLabels(implabel, labels) 
	#impOneNuc.show()
	impProj = maxZprojection( impOneNuc )
	ip = impProj.getProcessor()
	ip.setThreshold(nucID, nucID, ip.NO_LUT_UPDATE)
	roinuc = ThresholdToSelection.run(impProj)
	impProj.setRoi(roinuc)
	stats = ip.getStats()
#	print "nucx", stats.roiX
#	print "nucy", stats.roiY
#	print "nucw", stats.roiWidth
#	print "nuch", stats.roiHeight
	roibound = Roi(stats.roiX-offset, stats.roiY-offset, stats.roiWidth+ 2*offset, stats.roiHeight+2*offset)
	return impProj, roibound

def extractNucs( imporg ):
	imps = ChannelSplitter.split( imporg )
	impnuc = imps[1].duplicate()
	gaussianBlurStack( impnuc )
	thresholdMomentStack( impnuc )
	implabeled = connectedComponentAnalysis3D( impnuc )
	sizeLimit = 1000
	implabeledFiltered = removeSmallOnes(implabeled, sizeLimit)
	implabeledFiltered2 = removeBorderNucs( implabeledFiltered )
	LabelImages.remapLabels(implabeledFiltered2)
	#implabeledFiltered2.show()
	
	sstats = StackStatistics(implabeledFiltered2 )
	print "Labels Count:", sstats.max
	labelCount = int(sstats.max)
	
	nucimpA = []
	for i in range(labelCount):
		nucID = i + 1
		impProj, roibound = getBoundingRoi( implabeledFiltered2, nucID)
		imporg.setRoi(roibound)
		impnuc = Duplicator().run(imporg)
		nucimpA.append( impnuc )
		#nuc.show()
	return nucimpA
	
imporg = IJ.openImage("/Users/miura/samples/NPC1.tif")
imporg.setMode(IJ.COMPOSITE)
nucimpA = extractNucs( imporg )
nucimpA[0].show()
nucimpA[4].show()
nucimpA[9].show()

