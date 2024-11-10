from ij import IJ
from ij.plugin import ChannelSplitter

#アクティブな画像を取得
imp = IJ.getImage()
imp_split = ChannelSplitter.split(imp)
#1番目のチャネル
imp_mCherry = imp_split[0].duplicate()
#２番目のチャネル
imp_mVenus = imp_split[1].duplicate()
 #結果の表示
imp_mCherry.show()
imp_mVenus.show()