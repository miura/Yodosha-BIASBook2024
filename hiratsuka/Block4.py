from ij import IJ
from ij.plugin import ChannelSplitter
from ij.plugin import ImageCalculator
from ij.plugin import Concatenator
from ij.plugin import HyperStackConverter

channelsplitter = ChannelSplitter() 
IC = ImageCalculator()
concatenator = Concatenator()
HSC = HyperStackConverter() #インスタンスの形成

imp = IJ.getImage()
imp_dim = imp.getDimensions()
print(imp_dim) #Channel,Z,Tの枚数などの表示
imp_split = channelsplitter.split(imp)
imp_mCherry = imp_split[0].duplicate()
imp_mVenus = imp_split[1].duplicate()
imp_add = imp_mCherry.duplicate()
IC.run("add stack", imp_add, imp_mVenus)
imp_concat = concatenator.run(imp_mCherry, imp_mVenus, imp_add)
imp_HSC = HSC.toHyperStack(imp_concat, 3, imp_dim[3], imp_dim[4], "xyztc", "grayscale") #Hyperstackへの変換
imp_HSC.show()
