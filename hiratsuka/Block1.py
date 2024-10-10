from ij import IJ
from ij.plugin import ChannelSplitter

channelsplitter = ChannelSplitter() #インスタンスを作成
imp = IJ.getImage() #アクティブな画像を取得
imp_split = channelsplitter.split(imp)
imp_mCherry = imp_split[0].duplicate() #1番目のチャネル
imp_mVenus = imp_split[1].duplicate() #２番目のチャネル
imp_mCherry.show() #結果の表示
imp_mVenus.show() #結果の表示

