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

from ij import IJ

#　ガウスぼかしの関数
def Gaussian_filter(imp,sigma):
	if sigma > 0:
		print "Gaussian Blur: sigma: " + str(sigma)
	IJ.run(imp, "Gaussian Blur...", \
		"sigma=" + str(sigma) + " stack")
