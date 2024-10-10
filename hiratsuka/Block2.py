from ij import IJ
from ij.plugin import ChannelSplitter
from ij.plugin import ImageCalculator

channelsplitter = ChannelSplitter() 
IC = ImageCalculator() #ImageCalculatorのインスタンスを作成

imp = IJ.getImage() #アクティブな画像を取得
imp_split = channelsplitter.split(imp)
imp_mCherry = imp_split[0].duplicate() #チャネル１
imp_mVenus = imp_split[1].duplicate() #チャネル２
imp_add = imp_mCherry.duplicate() #複製
IC.run("add stack", imp_add, imp_mVenus)
#結果は複製したimp_addに上書きされる

imp_add.show() #結果の表示
