from ij import IJ, ImagePlus
from sc.fiji.analyzeSkeleton import AnalyzeSkeleton_

def analyzeSkeleton3D( skelimp ):
	skel = AnalyzeSkeleton_()
	skel.setup("", skelimp)
	pruneIndex = AnalyzeSkeleton_.NONE
	pruneEnds = False
	shortPath = False
	origImp = None
	silent = True
	verbose = False
	skelResult = skel.run(pruneIndex, \\
		pruneEnds, shortPath, origImp, silent, verbose)
	return skel, skelResult
	
skelimp = ImagePlus(\\
	"/Users/miura/samples/BloodVessels_small_skel.tif")
cal = skelimp.getCalibration()

skel, skelResult = analyzeSkeleton3D( skelimp )
skeletons = skelResult.getGraph()
juncNums = skelResult.getJunctions()
### stats ###
imWidth = skelimp.getWidth() * cal.pixelWidth
imHeight = skelimp.getHeight() * cal.pixelHeight
imDepth = skelimp.getNSlices() * cal.pixelDepth
totalVolume = imWidth * imHeight * imDepth #um^3
totalVolume = totalVolume / pow(1000, 3) #mm^3
# standard deviation
def sd( l ):
	mean = float(sum(l))/len(l)
	ss = sum((x-mean)**2 for x in l)
	sd = (ss/(len(l)-1))**0.5
	return sd
#tortuosity
def calcTortuosity(edge):
	length = edge.getLength()
	v1p = edge.getV1().getPoints().get(0)
	v2p = edge.getV2().getPoints().get(0)
	dist = skel.calculateDistance(v1p, v2p)
	tortuosity = length/dist
	return tortuosity

Alltortuosity = []
AllBranchLen = []
for s in skeletons:
	edgeList = s.getEdges()
	tortuosityA = map(calcTortuosity, edgeList)
	Alltortuosity += tortuosityA
	branchLengthA = map(\\
		lambda e:e.getLength(), edgeList)
	AllBranchLen += branchLengthA

totalBranchlens = sum(AllBranchLen)
totalBranchNum = len(AllBranchLen)
ave_BranchLen = totalBranchlens / totalBranchNum
sd_BranchLen = sd(AllBranchLen)
branchDensity = totalBranchNum / totalVolume
vesselLengthDensity = totalBranchlens / totalVolume
totaljuncs = sum(juncNums)
junctionDensity = totaljuncs / totalVolume
ave_tortuosity = sum(Alltortuosity) / len(Alltortuosity)

print("Image Width: " + str(imWidth) +  " (um)")
print("Total Imaged Volume: " + \\
	str(totalVolume) + " (mm^3)")
print("Total Branch Length: " + \\
	str(totalBranchlens) + " (um)")
print("Total Branch Number: " + \\
	str(totalBranchNum))
print("Average Branch Length: " + \\
	str(ave_BranchLen) + " (um)")
print("... standard deviation: " + \\
	str(sd_BranchLen) + " (um)")
print("Branch Density: " + \\
	str(branchDensity) + " (/mm^3)")
print("Vessel Length Density: " + \\
	str(vesselLengthDensity/1000) + \\
		" (mm/mm^3)")
print("Total Junction Number: " + \\
	str(totaljuncs))
print("Junction Density: " + \\
	str(junctionDensity) + " (/mm^3)")
print("Average Tortuosity: " + str(ave_tortuosity))

### visualization
import  Replace_Value
from ij.plugin import LutLoader
from ij.process import LUT
from ij.plugin import LutLoader
from inra.ijpb.binary.distmap import ChamferMask3D
from inra.ijpb.label.filter import ChamferLabelDilation3DShort
from ij.process import ImageConverter
from ij3d import Image3DUniverse

# tagged image visualization
tagstack = skel.getResultImage(False)
tagimp = ImagePlus("tagged", tagstack)

rv = Replace_Value()
rv.setup(None, tagimp)
rv.doit(70, 215)
rv.doit(30, 250)

radius = 1.0
algo = ChamferLabelDilation3DShort(\\
	ChamferMask3D.SVENSSON_3_4_5_7, radius)
tagstackDilated = algo.process(tagstack)
tagDilatedimp = ImagePlus("tagDilated", tagstackDilated)

fireLL = LutLoader.getLut("fire")
fireLut = LUT(fireLL, float(0), float(255))
tagDilatedimp.setLut(fireLut)

univ = Image3DUniverse()
c = univ.addVoltex(tagDilatedimp)
univ.show()

# labeled image visualization
labelstack = skel.getLabeledSkeletons()
labelstack = algo.process(labelstack)
labelimp = ImagePlus("labeled", labelstack)
currentState = ImageConverter.getDoScaling()
ImageConverter.setDoScaling(False)
ImageConverter(labelimp).convertToGray8()
ImageConverter.setDoScaling(currentState)

giLut = LutLoader.getLut("Glasbey on Dark")
labelimp.setLut(giLut)

univ2 = Image3DUniverse()
c2 = univ2.addVoltex(labelimp)
univ2.show()



    

