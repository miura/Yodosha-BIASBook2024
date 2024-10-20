from ij import ImagePlus
from ij.gui import Line
from ij.gui import ProfilePlot

imp = ImagePlus( "/Users/miura/blobs.tif" )
lineRoi = Line(140, 20, 140, 230)
imp.setRoi(lineRoi)
pf = ProfilePlot(imp)
profile = pf.getProfile()
for val in profile:
	print( val )
	
import csv

f = open('/Users/miura/Desktop/prof.csv', 'wb')
writer = csv.writer(f)
for index, val in enumerate(profile):
	writer.writerow([index, val])

f.close()