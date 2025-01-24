#@ File (label = "Input directory", style = "directory") srcFile
#@ File (label = "Output directory", style = "directory") dstFile
#@ String (label = "File extension", value=".tif") ext
#@ String (label = "File name contains", value = "") containString
#@ Integer (label = "Background subtraction (Disabled if 0)", value = 50) BGval
#@ Integer (Label = "3D filter (Disabled if 0)", value = 1) sigma

#------------Trackmateのパラメータ-----------
SegCh = 3
Threshold = 0.1 
CellSize = 20.0
LinkMaxDis = 25.0
GapClosingMaxDis = 50.0
MaxFrameGap = 2

import os
import sys
from ij import IJ
from fiji.plugin.trackmate \
	import 	Settings, \
			Model, \
			TrackMate, \
			Logger
from fiji.plugin.trackmate.detection \
	import	DetectorKeys, \
			LogDetectorFactory
from fiji.plugin.trackmate.tracking.jaqaman \
	import  LAPUtils, \
			SimpleSparseLAPTrackerFactory
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from ij.process import StackStatistics
from ij.plugin import \
	ChannelSplitter, \
	ImageCalculator, \
	Concatenator,  \
	HyperStackConverter
import csv

#インスタンスの作成
IC = ImageCalculator()

#ポップアップアップウインドウで取得した情報
	#探索するフォルダの絶対パスを取得
srcDir = srcFile.getAbsolutePath()
	#画像を保存するフォルダの絶対パスを取得
dstDir = dstFile.getAbsolutePath()
print srcDir + str(srcDir)
print dstDir + str(dstDir)

#-------関数の記述ここから-------------
# Image Importerによる画像の読み込みを行う関数
def IOimp(dirname, filename):
  io = ImporterOptions()
  io.setOpenAllSeries(False)
  io.setConcatenate(False)
  io.setId((os.path.join(dirname, filename)))
  print "Opening image file: ", filename
  imps = BF.openImagePlus(io)
  print imps
  return imps[0]

# 残りの関数は省略(サポートレポジトリ参照)
#-------関数の記述ここまで-------------

#  条件を満たすファイルの探索と処理
for root, directories, filenames in os.walk(srcDir):
	filenames.sort()
	for filename in filenames:
		#拡張子のチェック
		if not filename.endswith(ext): 
			continue
		#ファイル名のチェック
		if containString not in filename:
			continue
		#ファイルのディレクトリを表示
		print(os.path.join(root,filename))
		imp = IOimp(root,filename)		
		#  ファイル一つの前処理	
		imp_HSC = prepare3chHyperstack(imp)
		#処理後の画像の保存	
		if not os.path.exists(dstDir):
		  os.makedirs(dstDir)
		print "Saving to", dstDir
		savefilename = filename.replace("." + ext, "")
		IJ.saveAs(imp_HSC, "Tiff", \
			os.path.join(dstDir, savefilename))		
		#Trackmate解析と結果の保存
		model = Trackmate_analysis(imp_HSC)
		saveOutputs(imp_HSC, model )

IJ.log("Analysis completed. \
		Please check the destination directory \
		for saved images and quantification data.")
