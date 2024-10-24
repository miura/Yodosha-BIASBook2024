from ij import IJ
from ij.plugin import ChannelSplitter
from ij.plugin import ImageCalculator
from ij.plugin import Concatenator
from ij.plugin import HyperStackConverter

#インスタンスの形成
IC = ImageCalculator()

imp = IJ.getImage()
imp_dim = imp.getDimensions()
#Channel,Z,Tの枚数などの表示
print(imp_dim)
imp_split = ChannelSplitter.split(imp)
imp_mCherry = imp_split[0].duplicate()
imp_mVenus = imp_split[1].duplicate()
imp_add = imp_mCherry.duplicate()
IC.run("add stack", imp_add, imp_mVenus)
imp_concat = Concatenator.\
           run(imp_mCherry, imp_mVenus, imp_add)
#Hyperstackへの変換
imp_HSC = HyperStackConverter.\
        toHyperStack(imp_concat, 3, \
        imp_dim[3], imp_dim[4], \
        "xyztc", "grayscale")

#結果の表示
imp_HSC.show()
