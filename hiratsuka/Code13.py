#@ File (label = "Input directory", style = "directory") srcFile
#@ File (label = "Output directory", style = "directory") dstFile
#@ String (label = "File extension", value=".tif") ext
#@ String (label = "File name contains", value = "") containString
#@ Integer (label = "Background subtraction (Disabled if 0)", value = 50) BGval
#@ Integer (label = "3D filter (Disabled if 0)", value = 1) sigma

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

#  ファイル一つの前処理
def prepare3chHyperstack(imp):
	imp_mCherry, imp_mVenus, imp_add = split_and_add(imp)
	Gaussian_filter(imp_add,sigma)
	Background_subtraction(imp_add,BGval)
	Baseline_subtraction(imp_mCherry)
	Baseline_subtraction(imp_mVenus)
	imp_HSC = concat_HSC(imp_mCherry,imp_mVenus,imp_add)
	return imp_HSC
	
# Trackmateで解析を行う関数
def Trackmate_analysis(Tracking_Image):

	#-----------追跡モデルのインスタンス化--------------  
	model = Model()
	model.setLogger(Logger.IJ_LOGGER) # Set logger
	settings = Settings(Tracking_Image)

	# -----------検出器のインスタンス化と設定-----------
	settings.detectorFactory = \
			LogDetectorFactory()
	settings.detectorSettings.\
		put('DO_SUBPIXEL_LOCALIZATION', True)
	settings.detectorSettings.\
		put('RADIUS', CellSize/2)
	settings.detectorSettings.\
		put('TARGET_CHANNEL', SegCh)
	settings.detectorSettings.\
		put('THRESHOLD', Threshold)
	settings.detectorSettings.\
		put('DO_MEDIAN_FILTERING', False) 

	# -----------追跡器のインスタンス化と設定------------
	settings.trackerFactory = \
			SimpleSparseLAPTrackerFactory()
	settings.trackerSettings \
		= LAPUtils.getDefaultSegmentSettingsMap()
	settings.trackerSettings.\
		put('LINKING_MAX_DISTANCE', LinkMaxDis)
	settings.trackerSettings.\
		put('GAP_CLOSING_MAX_DISTANCE', GapClosingMaxDis)
	settings.trackerSettings.\
		put('MAX_FRAME_GAP', MaxFrameGap)
	settings.addAllAnalyzers()

	#------------Trackmateのインスタンス化--------------
	trackmate = TrackMate(model, settings)

	#------------Trackmateの実行----------------------    
	ok = trackmate.checkInput()
	if not ok:
		sys.exit(str(trackmate.getErrorMessage())) 
	ok = trackmate.process()
	if not ok:
		sys.exit(str(trackmate.getErrorMessage()))     
 
	return model
	
# Trackmateの結果を出力する関数
def saveOutputs( Tracking_Image, model ):
	nChannels = Tracking_Image.getDimensions()[2]
	imageTitle = Tracking_Image.getTitle()
	#出力ファイルの名前の構築
	basename = os.path.splitext(imageTitle)[0]
	intensitiesFileName = os.path.join(str(dstFile), \
		basename + "_Intensities.csv")
	logFileName = os.path.join(str(dstFile), \ 
		basename + "_log.txt")

	#------------ 検出点の特徴量を出力------------------
	f = open(intensitiesFileName, 'wb')
	writer = csv.writer(f)
	header = ['Spot', 'TrackID', 'X', 'Y', 'Q', 'Z', 'T']
	for i in range(nChannels):
		header.append('C' + str(i+1))
	writer.writerow(header)
	
	for id in model.getTrackModel().trackIDs(True):
		track = model.getTrackModel().trackSpots(id)
		if len(track) > 0:
			for spot in track:
				AllValues = [  \
				spot.ID(),id, \
				spot.getFeature('POSITION_X'), \
				spot.getFeature('POSITION_Y'), 
				spot.getFeature('QUALITY'), \
				spot.getFeature('POSITION_Z'), 
				spot.getFeature('FRAME') \
				]
				for i in range(nChannels):
					AllValues.append(\
					spot.getFeature('MEAN_INTENSITY_CH%01d' % (i+1)))				
				writer.writerow(AllValues)
	f.close()

	#------------ Save Values ------------------
	logf = open(logFileName, 'wb')
	logtext = IJ.getLog()
	logf.write(logtext)
	logf.close()
	IJ.log("\\Clear")

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
