from ij import IJ
from ij.plugin import ChannelSplitter
from ij.plugin import ImageCalculator

#インスタンスを作成
IC = ImageCalculator()

#アクティブな画像を取得
imp = IJ.getImage()
imp_split = ChannelSplitter.split(imp)
#チャネル１
imp_mCherry = imp_split[0].duplicate()
#チャネル２
imp_mVenus = imp_split[1].duplicate()
#複製
imp_add = imp_mCherry.duplicate() 
IC.run("add stack", imp_add, imp_mVenus)
#結果は複製したimp_addに上書きされる

 #結果の表示
imp_add.show()
