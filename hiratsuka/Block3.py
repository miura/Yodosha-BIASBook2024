from ij import IJ
from ij.plugin import ChannelSplitter
from ij.plugin import ImageCalculator
from ij.plugin import Concatenator

channelsplitter = ChannelSplitter() 
IC = ImageCalculator()
concatenator = Concatenator() #インスタンスの作成

imp = IJ.getImage()
imp_split = channelsplitter.split(imp)
imp_mCherry = imp_split[0].duplicate() #チャネル１
imp_mVenus = imp_split[1].duplicate() #チャネル２
imp_add = imp_mCherry.duplicate()
IC.run("add stack", imp_add, imp_mVenus) #チャネル３

imp_concat = concatenator.run(imp_mCherry, imp_mVenus, imp_add)
#連結した画像
imp_concat.show() #結果の表示
