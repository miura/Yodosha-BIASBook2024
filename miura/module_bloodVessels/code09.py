# code09: measure single nucleus time series
from ij import IJ
from ij import ImagePlus
from ij.process import ImageProcessor
from ij.plugin import ImageCalculator
from ij.plugin import ChannelSplitter
from ij.plugin import Duplicator
from ij.plugin.filter import GaussianBlur
from ij.plugin.filter import Binary
from ij.plugin.filter import ThresholdToSelection
from fiji.threshold import Auto_Threshold
from inra.ijpb.morphology import Reconstruction

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
def measureSingleNucleus( orgimp ):
  impLamine, impNuc = splitChannels( orgimp )
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
  
nucImagePath = "/Users/miura/samples/NPC1n1.tif"
orgimp = IJ.openImage( nucImagePath )
pixcountA, meanA, totalA = measureSingleNucleus( orgimp )
print pixcountA
print meanA
print totalA