from ij import IJ
from ij.plugin import \
	ChannelSplitter, \
	ImageCalculator

#インスタンスを作成
IC = ImageCalculator()

#　チャネルを分割し、重ね合わせ画像を作成する関数
def split_and_add(imp):
	imp_split = ChannelSplitter.split(imp)
	imp_mCherry = imp_split[0].duplicate()
	imp_mVenus = imp_split[1].duplicate()
	imp_add = imp_mCherry.duplicate()
	IC.run("add stack", imp_add, imp_mVenus)
	return imp_mCherry, imp_mVenus, imp_add

#アクティブな画像を取得
imp = IJ.getImage()
imp_mCherry, imp_mVenus, imp_add = split_and_add(imp)
# 　画像を表示
imp_mCherry.show()
imp_mCherry.setTitle('mCherry')
imp_mVenus.show()
imp_mVenus.setTitle('mVenus')
imp_add.show()
imp_add.setTitle('Add')

#@ Integer (Label = "Gaussian Blur (Disabled if 0)", value = 1) sigma

#　ガウスぼかしの関数
def Gaussian_filter(imp,sigma):
	if sigma > 0:
		print "Gaussian Blur: sigma: " + str(sigma)
	IJ.run(imp, "Gaussian Blur...", \
		"sigma=" + str(sigma) + " stack")
		
Gaussian_filter(imp_add, sigma)

#@ Integer (label = "Background subtraction (Disabled if 0)", value = 50) BGval

#　背景の引き算処理の関数
def Background_subtraction(imp,BGval):
	if BGval >0:
		print "Background subtraction: rolling ball: " \
			+ str(BGval)
		IJ.run(imp, "Subtract Background...", \
			"rolling=" + str(BGval) + " stack")

Background_subtraction(imp_add, BGval)

from ij.process import StackStatistics

#　ベースライン輝度の引き算の関数
def Baseline_subtraction(imp):
	stat_imp = StackStatistics(imp)
	minVal_imp = stat_imp.min
	IJ.run(imp, "Subtract...", \
	"value=" + str(minVal_imp) + " stack")

Baseline_subtraction(imp_mCherry)
Baseline_subtraction(imp_mVenus)
