from ij.process import StackStatistics
from ij import IJ
imp = IJ.getImage()
#スタック画像全体での統計量の取得
stat = StackStatistics(imp)
#スタック画像全体での最小値
minVal = stat.min
#最小値をバックグラウンドとして画像全体から引き算する
IJ.run(imp, "Subtract...", "value=" + str(minVal) + " stack");