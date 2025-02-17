#@ Integer (label = "Background subtraction (Disabled if 0)", value = 50) BGval
#@ Integer (label = "3D filter (Disabled if 0)", value = 1) sigma

#モジュールのimport
import os
import sys
from ij import IJ, ImagePlus
from ij.process import StackStatistics
from ij.plugin import \
	ChannelSplitter, \
	ImageCalculator, \
	Concatenator,  \
	HyperStackConverter

#インスタンスの作成
IC = ImageCalculator()

#-------これまでの関数の記述ここから-------------
# 省略(サポートレポジトリ参照)
#-------これまでの関数の記述ここまで-------------

#  ファイル一つの前処理の関数
def prepare3chHyperstack(imp):
	#　チャネルを分割し、重ね合わせ画像を作成
	imp_mCherry, imp_mVenus, imp_add = split_and_add(imp)
	#　ガウスぼかしの関数を重ね合わせ画像に適用
	Gaussian_filter(imp_add,sigma)
	#　背景の引き算処理の関数をさらに適用
	Background_subtraction(imp_add,BGval)
	#　ベースライン輝度の引き算の関数を
	#  mCherry画像とmVenus画像に適用
	Baseline_subtraction(imp_mCherry)
	Baseline_subtraction(imp_mVenus)
	# 　連結画像を作成
	imp_HSC = concat_HSC(imp_mCherry,imp_mVenus,imp_add)
	return imp_HSC

#　アクティブな画像を取得
imp = IJ.getImage()
#  ファイル一つの前処理
imp_HSC = prepare3chHyperstack(imp)
imp_HSC.show()
