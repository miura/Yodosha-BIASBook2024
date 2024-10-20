from ij import ImagePlus
from ij.gui import Line
from ij.gui import ProfilePlot
import csv

def getProfile(imp):
	pf = ProfilePlot(imp)
	profile = pf.getProfile()
	for val in profile:
		print( val )
	return profile
	

def writeProfileToFile(writepath, profile):
	f = open(writepath, 'wb')
	writer = csv.writer(f)
	for index, val in enumerate(profile):
		writer.writerow([index, val])
	f.close()

writepath = "/Users/miura/Desktop/prof.csv"
imp = ImagePlus( "/Users/miura/blobs.tif" )
lineRoi = Line(140, 20, 140, 230)
imp.setRoi(lineRoi)

profile = getProfile(imp)
writeProfileToFile(writepath, profile)
