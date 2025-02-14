#@ Integer (label = "Background subtraction (Disabled if 0)", value = 50) BGval
#@ Integer (Label = "3D filter (Disabled if 0)", value = 1) sigma

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

#　チャネルを分割し、重ね合わせ画像を作成する関数
def split_and_add(imp):
	imp_split = ChannelSplitter.split(imp)
	imp_mCherry = imp_split[0].duplicate()
	imp_mVenus = imp_split[1].duplicate()
	imp_add = imp_mCherry.duplicate()
	IC.run("add stack", imp_add, imp_mVenus)
	return imp_mCherry, imp_mVenus, imp_add

#　ガウスぼかしの関数
def Gaussian_filter(imp,sigma):
	if sigma > 0: 
		print "Gaussian Blur: sigma: " + str(sigma)   
		IJ.run(imp, "Gaussian Blur...", \
			"sigma=" + str(sigma) + " stack")

#　背景の引き算処理の関数
def Background_subtraction(imp,BGval):
	if BGval >0: 
		print "Background subtraction: rolling ball: " \
			+ str(BGval)
		IJ.run(imp, "Subtract Background...", \
			"rolling=" + str(BGval) + " stack")

#　ベースライン輝度の引き算の関数
def Baseline_subtraction(imp):
	stat_imp = StackStatistics(imp)
	minVal_imp = stat_imp.min
	IJ.run(imp, "Subtract...", \
	"value=" + str(minVal_imp) + " stack")

#　連結画像を作成する関数
def concat_HSC(imp1,imp2,imp3):
	imp_dim = imp1.getDimensions()
	#Channel,Z,Tの枚数などの表示
	print(imp_dim)
	imp_concat = Concatenator.run(imp1, imp2, imp3)
	#Hyperstackへの変換
	imp_HSC = HyperStackConverter.\
	toHyperStack(imp_concat, 3, \
	imp_dim[3], imp_dim[4], \
	"xyztc", "grayscale")
	return imp_HSC
	
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
