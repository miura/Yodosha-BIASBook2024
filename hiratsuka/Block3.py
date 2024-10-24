from ij import IJ
from ij.plugin import ChannelSplitter
from ij.plugin import ImageCalculator
from ij.plugin import Concatenator

#インスタンスの作成
IC = ImageCalculator()

imp = IJ.getImage()
imp_split = ChannelSplitter.split(imp)
#チャネル１
imp_mCherry = imp_split[0].duplicate()
#チャネル２
imp_mVenus = imp_split[1].duplicate()
imp_add = imp_mCherry.duplicate()
#チャネル３
IC.run("add stack", imp_add, imp_mVenus)

imp_concat = Concatenator.\
           run(imp_mCherry, imp_mVenus, imp_add)
#連結した画像

#結果の表示
imp_concat.show()
