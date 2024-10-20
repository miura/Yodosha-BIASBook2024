from ij import ImagePlus
from inra.ijpb.binary import BinaryImages
from inra.ijpb.label.select import LabelSizeFiltering
from inra.ijpb.label.select import RelationalOperator
from ij.plugin import LutLoader

def filterLabelTubes(binimp, sizeLimit):
	labeledimp = BinaryImages.componentsLabeling\
		(binimp, connectivity, bitdepth)
	gilut = LutLoader.getLut("glasbey_inverted")
	labeledimp.setLut(gilut)
	sizeFilter = LabelSizeFiltering\
		(RelationalOperator.GT, sizeLimit)
	filteredlabeledimp = sizeFilter.process(labeledimp)
	return filteredlabeledimp

connectivity = 26
bitdepth = 8
sizeLimit = 1000
filteredlabeledimp = filterLabelTubes(binimp, sizeLimit)
filteredlabeledimp.setTitle("BloodVessels_small_label.tif")
filteredlabeledimp.show()
