#@ File (label = "Input directory", style = "directory") srcFile
#@ File (label = "Output directory", style = "directory") dstFile
#@ String (label = "File extension", value=".tif") ext
#@ String (label = "File name contains", value = "") containString
#@ Integer (label = "Fucci Channel1 (1,2,3..)", value = 1) Fucci1
#@ Integer (Label = "Fucci Channel2 (1,2,3..)", value = 2) Fucci2
#@ Integer (label = "Background subtraction (Disabled if 0)", value = 50) BGval
#@ Integer (Label = "3D filter (Disabled if 0)", value = 1) sigma

#モジュールのimport
import os
import sys
from ij import IJ, ImagePlus
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from ij.plugin import ChannelSplitter
from ij.plugin import ImageCalculator
from ij.plugin import Concatenator
from ij.plugin import HyperStackConverter

#インスタンスの作成
channelsplitter = ChannelSplitter()
IC = ImageCalculator()
concatenator = Concatenator()
HSC = HyperStackConverter()

#ポップアップアップウインドウで取得した情報
srcDir = srcFile.getAbsolutePath() #探索するフォルダの絶対パスを取得
dstDir = dstFile.getAbsolutePath()#画像を保存するフォルダの絶対パスを取得
print srcDir + str(srcDir)
print dstDir + str(dstDir)

# Image Importerによる画像の読み込みを行う関数
def IOimp(dirname, filename):
  io = ImporterOptions()
  io.setOpenAllSeries(True)
  io.setConcatenate(False) 
  io.setId((os.path.join(dirname, filename)))
  print "Opening image file", filename
  imps = BF.openImagePlus(io)
  print imps
  return imps[0]

# 条件を満たすファイルの情報を初期化
filecol = []
rootcol = []
# 条件を満たすファイルの探索
for root, directories, filenames in os.walk(srcDir):
	filenames.sort()
	for filename in filenames:
		if not filename.endswith(ext): #拡張子のチェック
			continue
		if containString not in filename: #ファイル名のチェック
			continue
		filecol.append(filename)
		rootcol.append(root)

# 条件を満たす画像ファイルへの繰り返し処理
for i in range(len(filecol)):
  	print(os.path.join(rootcol[i],filecol[i])) #ファイルのディレクトリを表示
  	imp = IOimp(rootcol[i],filecol[i]) #画像を読み込み
  	imp_dim = imp.getDimensions()
  	imp_split = channelsplitter.split(imp)
  	imp_mCherry = imp_split[0].duplicate()
  	imp_mVenus = imp_split[1].duplicate()
  	imp_add = imp_mCherry.duplicate()
  	IC.run("add stack", imp_add, imp_mVenus)
  	imp_concat = concatenator.run(imp_mCherry, imp_mVenus, imp_add)
  	imp_HSC = HSC.toHyperStack(imp_concat, 3, imp_dim[3], imp_dim[4], "xyztc", "grayscale")
  	if BGval >0: #バックグラウンド処理
		print "Background subtraction: rolling ball: " + str(BGval)
		IJ.run(imp_HSC, "Subtract Background...", "rolling=" + str(BGval) + " stack")
	if sigma > 0: #ガウスぼかし処理
		print "Gaussian Blur: sigma: " + str(sigma)   
		IJ.run(imp, "Gaussian Blur...", "sigma=" + str(sigma) + " stack")

	#処理後の画像の保存
  	if not os.path.exists(dstDir):
  	  os.makedirs(dstDir)
  	print "Saving to", dstDir
  	savefilename = filecol[i].replace("." + ext, "")
  	#print savefilename
  	IJ.saveAs(imp_HSC, "Tiff", os.path.join(dstDir, savefilename));
  	imp_HSC.close()
