#@ File (label = "Output directory", style = "directory") dstFile

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
import csv

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
					AllValues.append(\			spot.getFeature('MEAN_INTENSITY_CH%01d' % (i+1)))
				
				writer.writerow(AllValues)
	f.close()

	#------------ Save Values ------------------
	logf = open(logFileName, 'wb')
	logtext = IJ.getLog()
	logf.write(logtext)
	logf.close()
	IJ.log("\\Clear")
	
imp3ch = IJ.getImage()
model = Trackmate_analysis( imp3ch )
saveOutputs( imp3ch, model )
