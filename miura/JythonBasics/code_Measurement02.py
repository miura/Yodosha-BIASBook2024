from ij import IJ, ImagePlus
from ij.plugin.filter import Analyzer
from ij.measure import ResultsTable

imp = ImagePlus( "/Users/miura/bat-cochlea-volume.tif" )
frames = imp.getStackSize()
rt =  ResultsTable()
ana = Analyzer ( imp , rt)
ana.setMeasurements(Analyzer.MEAN + Analyzer.SLICE)
for i in range(frames):
	imp.setSlice(i + 1)
	ana.measure()
rt.show("Measurements")

	