#@ File (label = "Input directory", style = "directory") srcFile
#@ File (label = "Output directory", style = "directory") dstFile
#@ String (label = "File extension", value=".tif") ext
#@ String (label = "File name contains", value = "") containString
#@ Integer (label = "Fucci Channel1 (1,2,3..)", value = 1) Fucci1
#@ Integer (Label = "Fucci Channel2 (1,2,3..)", value = 2) Fucci2
#@ Integer (label = "Background subtraction (Disabled if 0)", value = 50) BGval
#@ Integer (Label = "3D filter (Disabled if 0)", value = 1) sigma

#------------Trackmate parameters-----------
# [Note] Check if each parameter is Integer or Long (10 or 10.0)!
SegCh = 3
#SegCh = 3
Threshold = 0.1 
CellSize = 20.0
SplittingMaxDis = 25.0
LinkMaxDis = 25.0
GapClosingMaxDis = 50.0
MaxFrameGap = 2
# Select from ['DoG Detector', 'LoG Detector']
Detector = 'LoG Detector'
# Select from ['Sparce LAP Tracker', 'Simple Sparce LAP Tracker']
Tracker = 'Simple Sparce LAP Tracker'
# Simple Sparce LAP Tracker cannot be used 
# when AllowSplitting is True
AllowSplitting = False
#------------Trackmate parameters-----------

#モジュールのimport
import os
import sys
from ij import IJ, ImagePlus
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from ij.process import StackStatistics
from ij.plugin import \
	ChannelSplitter, \
	ImageCalculator, \
	Concatenator,  \
	HyperStackConverter

from fiji.plugin.trackmate \
	import 	Settings, \
			Model, \
			TrackMate, \
			SelectionModel, \
			Logger
from fiji.plugin.trackmate.detection \
	import	DetectorKeys, \
			DogDetectorFactory, \
			LogDetectorFactory
from fiji.plugin.trackmate.tracking.jaqaman \
	import  LAPUtils, \
			SimpleSparseLAPTrackerFactory, \
			SparseLAPTrackerFactory
from ij.measure import ResultsTable
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

# ファイル一つの処理の関数
def prepare3chHyperstack( imp ):
	imp_dim = imp.getDimensions()
	imp_split = ChannelSplitter.split(imp)
	imp_mCherry = imp_split[0].duplicate()
	imp_mVenus = imp_split[1].duplicate()
	imp_add = imp_mCherry.duplicate()
	IC.run("add stack", imp_add, imp_mVenus)

	#バックグラウンド処理
	if BGval >0: 
		print "Background subtraction: rolling ball: " \
			+ str(BGval)
		IJ.run(imp_add, "Subtract Background...", \
			"rolling=" + str(BGval) + " stack")
			
	#ベースライン輝度の引き算
	stat_mCherry = StackStatistics(imp_mCherry)
	stat_mVenus = StackStatistics(imp_mVenus)
	minVal_mCherry = stat_mCherry.min
	minVal_mVenus = stat_mVenus.min
	IJ.run(imp_mCherry, "Subtract...", \
	"value=" + str(minVal_mCherry) + " stack")
	IJ.run(imp_mVenus, "Subtract...", \
	"value=" + str(minVal_mVenus) + " stack")
	print("Baselines: mCherry=" + str(minVal_mCherry) +\
		"mVenus=" + str(minVal_mVenus))
	#ガウスぼかし処理
	if sigma > 0: 
		print "Gaussian Blur: sigma: " + str(sigma)   
		IJ.run(imp_add, "Gaussian Blur...", \
			"sigma=" + str(sigma) + " stack")
	
	imp_concat = Concatenator.\
		run(imp_mCherry, imp_mVenus, imp_add)
	imp_HSC = HyperStackConverter.\
		toHyperStack(imp_concat, \
		3, imp_dim[3], imp_dim[4], \
		"xyztc", "grayscale")
	return imp_HSC

# Trackmateで解析を行う関数
def Trackmate_analysis(Tracking_Image):

	nChannels = Tracking_Image.	getDimensions()[2]
	imageTitle = Tracking_Image.getTitle()

	#-----------Model configuration-----------------   
	model = Model()
	model.setLogger(Logger.IJ_LOGGER) # Set logger
	settings = Settings(Tracking_Image)
	#-----------Model configuration-----------------  

	# -----------Detector configuration-----------------
	if Detector == 'DoG Detector': 
		settings.detectorFactory = DogDetectorFactory()
	elif Detector == 'LoG Detector':  
		settings.detectorFactory = LogDetectorFactory()
	else: sys.exit('No Detector Found')

	settings.detectorSettings = {
    	DetectorKeys.KEY_DO_SUBPIXEL_LOCALIZATION : True,
    	DetectorKeys.KEY_RADIUS : CellSize/2,
    	DetectorKeys.KEY_TARGET_CHANNEL : SegCh,
    	DetectorKeys.KEY_THRESHOLD : Threshold,
    	DetectorKeys.KEY_DO_MEDIAN_FILTERING : False,
	}   
	# -----------Detector configuration-----------------

	# -----------Tracker configuration-----------------
	if Tracker == 'Simple Sparce LAP Tracker':
		settings.trackerFactory = SimpleSparseLAPTrackerFactory()
	elif Tracker == 'Sparce LAP Tracker':
		settings.trackerFactory = SparseLAPTrackerFactory()
	else : sys.exit('No Tracker Found')

	settings.trackerSettings = LAPUtils.getDefaultSegmentSettingsMap()
	settings.trackerSettings['LINKING_MAX_DISTANCE'] = LinkMaxDis
	settings.trackerSettings['GAP_CLOSING_MAX_DISTANCE'] = GapClosingMaxDis
	settings.trackerSettings['MAX_FRAME_GAP']= int(MaxFrameGap)
	settings.trackerSettings.put('ALLOW_TRACK_SPLITTING', AllowSplitting)	# Cell division considered
	settings.trackerSettings['SPLITTING_MAX_DISTANCE']= SplittingMaxDis
	settings.trackerSettings.put('ALLOW_TRACK_MERGING', False) # Cell merge not considered
	settings.addAllAnalyzers()
	# -----------Tracker configuration-----------------

	#------------Instantiate trackmate-----------------
	trackmate = TrackMate(model, settings)
	#------------Instantiate trackmate-----------------

	#------------Execute Trackmate----------------------    
	ok = trackmate.checkInput()
	if not ok:
		sys.exit(str(trackmate.getErrorMessage())) 
	ok = trackmate.process()
	if not ok:
		sys.exit(str(trackmate.getErrorMessage()))     
	#------------Execute Trackmate----------------------    

	#------------Trackmate Results----------------------
	selectionModel = SelectionModel(model)
	#Contains Edge and track features
	fm = model.getFeatureModel()   
	#------------Trackmate Results----------------------

	#------------ Edge features results------------------
	EdgeTable = ResultsTable() 
	SourceList =[]
	TargetList =[]
	for edge in model.getTrackModel().edgeSet():
		SourceID = fm.getEdgeFeature(edge, 'SPOT_SOURCE_ID')
		TargetID = fm.getEdgeFeature(edge, 'SPOT_TARGET_ID')
		SourceList.append(SourceID)
		TargetList.append(TargetID)

	for i in range(len(SourceList)): 
		EdgeTable.incrementCounter() 
		EdgeTable.addValue('SPOT_SOURCE_ID', SourceList[i])  
		EdgeTable.addValue('SPOT_TARGET_ID', TargetList[i]) 
	EdgeTable.show('Edge List')
	#------------ Edge features results------------------

	#------------ Spot features results------------------
	basename = os.path.splitext(imageTitle)[0]
	intensitiesFileName = os.path.join(str(dstFile), \
		basename + "_Intensities.csv")
	f = open(intensitiesFileName, 'wb')
	writer = csv.writer(f)
	header = ['Spot', 'TrackID', 'X', 'Y', 'Q', 'Z', 'T']
	for i in range(nChannels):
		header.append('C' + str(i+1))
	writer.writerow(header)
	
#	headerStr = '%s %10s %10s %10s %10s %10s %10s %10s' % \
#		('Spot', '#Track', 'X', 'Y', 'Q', 'Z', 'R', 'T')
#	rowStr = '%d %10d %10.1f %10.1f %10.1f %10.1f %10.1f'
#	for i in range(nChannels):
#		headerStr +=  ( ' %10s' % ( 'C' + str(i+1)))
#		rowStr += (' %10.1f')
#	model.getLogger().log(headerStr)
	
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
				
#				model.getLogger().log(rowStr % tuple(AllValues))
				writer.writerow(AllValues)
	f.close()
	#------------ Spot features results------------------

	#------------ Save Values ------------------
#	basename = os.path.splitext(imageTitle)[0]
	IJ.selectWindow("Log")
	IJ.saveAs("Text", os.path.join(str(dstFile), \ 
#		basename + "Spots.txt"))
		basename + "_log.txt"))
	IJ.run("Close")
	IJ.selectWindow("Edge List")
	IJ.saveAs("Text", os.path.join(str(dstFile), \
		basename + "_Edges.txt"))
	IJ.run("Close")
	#------------ Save Values ------------------

# 条件を満たすファイルの探索と処理
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
		imp_HSC = prepare3chHyperstack( imp )
		#処理後の画像の保存	
		if not os.path.exists(dstDir):
		  os.makedirs(dstDir)
		print "Saving to", dstDir
		savefilename = filename.replace("." + ext, "")
		IJ.saveAs(imp_HSC, "Tiff", \
			os.path.join(dstDir, savefilename))
		Trackmate_analysis(imp_HSC)
	IJ.log("Analysis completed. \
		Please check the destination directory \
		for images and quantifications.")
