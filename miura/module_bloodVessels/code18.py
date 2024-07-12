# code 18: nucleus rim intensity measurements
from java.awt import Color
from java.awt.image import ColorModel
from ij import IJ
from ij import ImagePlus
from ij.gui import Roi
from ij.process import ImageProcessor
from ij.process import StackStatistics
from ij.plugin import ImageCalculator
from ij.plugin import ChannelSplitter
from ij.plugin import Duplicator
from ij.plugin import CompositeConverter
from ij.plugin import ZProjector
from ij.plugin.filter import GaussianBlur
from ij.plugin.filter import Binary
from ij.plugin.filter import ThresholdToSelection
from fiji.threshold import Auto_Threshold
from inra.ijpb.morphology import Reconstruction
from inra.ijpb.label import LabelImages
from inra.ijpb.color.ColorMaps import CommonLabelMaps
from inra.ijpb.color import ColorMaps
from inra.ijpb.binary.conncomp import FloodFillComponentsLabeling3D
from inra.ijpb.plugins import RemoveBorderLabelsPlugin
from inra.ijpb.plugins import Connectivity3D
from inra.ijpb.plugins import LabelSizeFilteringPlugin
from inra.ijpb.plugins.LabelSizeFilteringPlugin import Operation

# orgimp: ImagePlus
def splitChannels( orgimp ):
  imps = ChannelSplitter.split( orgimp )
  impLamine = imps[0]
  impNuc = imps[1]
  return impLamine, impNuc
  
# Gaussian blur, blur slightly to attenuate noise
def gaussianBlur( impNuc ):
	impNucSeg = impNuc.duplicate()
	radius = 2.0
	accuracy = 0.01
	GaussianBlur().blurGaussian( impNucSeg.getProcessor(), radius, radius, accuracy)
	return impNucSeg

#Otsu Threshold
def thresholdOtsu( impNucSeg ):
	# get Otsu threshold value
	hist = impNucSeg.getProcessor().getHistogram()
	lowTH = Auto_Threshold.Otsu(hist)
	print "Otsu Threshold:", lowTH
	
	# create nucleus mask
	impNucSeg.getProcessor().threshold(lowTH)

# fill hole
def fillHole( impNucSeg ):
	binner = Binary()
	binner.setup("fill", None)
	binner.run(impNucSeg.getProcessor())

# remove unwanted nuclei (border nuclei)
def removeBorderNuc( impNucSeg ):
	ipSeg = Reconstruction.killBorders(impNucSeg.getProcessor())
	impNucSegFinal = ImagePlus("nucseg", ipSeg)
	return impNucSegFinal

# get the nucleus edge mask
def getEdgeMask( impNucSegFinal ):	
	impErode = impNucSegFinal.duplicate()
	binner = Binary()
	binner.setup("erode", None)
	binner.run(impErode.getProcessor())
	binner.run(impErode.getProcessor())
	impEdge = ImageCalculator().run("Subtract create", impNucSegFinal, impErode)
	return impEdge

# generate ROI from the binary image, and set the ROI to the Lamine image
def getEdgeROI( impEdge ):
	impEdge.getProcessor().setThreshold(255, 255, ImageProcessor.NO_LUT_UPDATE)
	roiEdge = ThresholdToSelection.run(impEdge)
	return roiEdge
#TimeSeries
# impNuc: nucleus image, 1ch, single time point
# returns a ROI at the nucleus edge
def getEdgeROISingle( impNuc ):
	impNucSeg = gaussianBlur( impNuc )
	thresholdOtsu( impNucSeg )
	fillHole( impNucSeg )
	impNucSegFinal = removeBorderNuc( impNucSeg )
	impEdge = getEdgeMask( impNucSegFinal )
	roiEdge = getEdgeROI( impEdge )
	return roiEdge

# impLamine: lamin image
# t: framenumber starting from 0
# roiEdge: Nucleus edge ROI
def measureNucEdge(impLamine, t, roiEdge):
	impLamine.setT( t + 1)
	impLamine.setRoi( roiEdge )
	
	#Measurements
	stats = impLamine.getRawStatistics()
	print "Frame:", t+1
	print "  Pix counts", stats.pixelCount
	print "  Mean", stats.mean
	print "  total intensity", stats.pixelCount * stats.mean
	return stats.pixelCount, stats.mean, stats.pixelCount * stats.mean

#nucImagePath: image path string
def measureSingleNucleus( nucImagePath ):
  impLamine, impNuc = splitChannels( nucImagePath )
  nframes = impNuc.getNFrames()
  pixcountA = []
  meanA = []
  totalA = []

  for t in range(nframes):
    impNucOneFrame = Duplicator().run(impNuc, t+1, t+1)
    roiEdge = getEdgeROISingle( impNucOneFrame )
    pixcount, mean, total = measureNucEdge(impLamine, t, roiEdge)
    pixcountA.append(pixcount)
    meanA.append(mean)
    totalA.append(total)
  
  return pixcountA, meanA, totalA
  

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
	colorMap = \
	   CommonLabelMaps.GLASBEY_BRIGHT.computeLut(255, False)
	cm = ColorMaps.createColorModel(colorMap, Color.BLACK)
	bitDepth = 8
	connectivity = "6"
	connValue = \
	   Connectivity3D.fromLabel(connectivity).getValue()
	algo = FloodFillComponentsLabeling3D(connValue, bitDepth)
	res = algo.computeResult(imp.getStack())
	implabeled = ImagePlus("labeled", res.labelMap)
	implabeled.getProcessor().setColorModel(cm)
	implabeled.getStack().setColorModel(cm)
	implabeled.setDisplayRange(0, max(res.nLabels, 255))
	return implabeled

#implabeled.show()

# size filtering
def removeSmallOnes(implabeled, sizeLimit):
	filtertype = "Greater_Than"
	op = Operation.fromLabel( filtertype )
	implabeledFiltered = op.applyTo(implabeled, sizeLimit)
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

import csv
outfilepath = "/Users/miura/samples/nucmeasures.csv"
f = open(outfilepath, 'wb')
writer = csv.writer(f)
writer.writerow(["NucleusID", "Frame", "PixArea", "Mean", "Total"])

for i, aimp in enumerate( nucimpA ):
	pixcountA, meanA, totalA = measureSingleNucleus( aimp )
	
	for ii in range(len(pixcountA)):
		row = [i+1, ii, pixcountA[ii], meanA[ii], totalA[ii]]
		writer.writerow(row)
		
	print "NUC", i
	print " ", pixcountA
	print " ", meanA
	print " ", totalA
	
f.close()