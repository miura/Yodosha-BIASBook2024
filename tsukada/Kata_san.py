from fiji.plugin.trackmate.visualization.hyperstack import HyperStackDisplayer
from fiji.plugin.trackmate.io import TmXmlReader
from fiji.plugin.trackmate.io import TmXmlWriter
from fiji.plugin.trackmate import Logger
from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate.gui.displaysettings import DisplaySettingsIO
from fiji.plugin.trackmate.visualization.trackscheme import TrackScheme
from java.io import File
import sys
 
# 文字コードを UTF8 に設定 
reload(sys)
sys.setdefaultencoding('utf-8') 

# スクリプトで読み込むTrackMateのモデルを保存したファイルのパス
# ファイルパスは自分の環境、ファイル位置に差し替えること
file = File( '/Users/yuki-ts/Documents/TrackMate/test.xml' )
 
# log 編集のための変数
logger = Logger.IJ_LOGGER

# ファイルを読み込むための readerの初期化
reader = TmXmlReader( file )
# ファイルがなければエラーを出力する
if not reader.isReadingOk():
    sys.exit( reader.getErrorMessage() )
 
# 読み込んだファイルからTrackMateのモデルを受け取る
# 値がないものはnullもしくはNone
# ここでのモデルはfiji.plugin.trackmate.Modelで定義される
model = reader.getModel()
 
# モデルの部分選択
sm = SelectionModel( model )
 
# 画面表示のための初期設定
ds = DisplaySettingsIO.readUserDefault()
 
# 読み込んだモデルを初期設定で表示
displayer =  HyperStackDisplayer( model, sm, ds ) 
displayer.render()

# モデルの中の追跡対象(spot)の集団をspotsとして抽出 
# spotsはfiji.plugin.trackmate.SpotCollectionで定義される
spots = model.getSpots()

# 抽出したspotsをログに記述
logger.log( str(spots) )
 
# TrackMateのフィルタ で選別された追跡対象(spot)のみ抽出し、
# ログに記述
trackIDs = model.getTrackModel().trackIDs(True) # only filtered out ones
for id in trackIDs:
    logger.log( str(id) + ' - ' + str(model.getTrackModel().trackEdges(id)) )
 
# 画像ファイルを読み込み変数impに格納する
# 先に読み込んだXMLに記述されている場所を参照するため、画像ファイルを
# 移動すると不具合がでる
imp = reader.readImage()
 
# 画像のためのの設定も読み込みsettingsに格納する
settings = reader.readSettings( imp )
# ついでに画像のフレーム数を取得
NumFrame = settings.nframes

# 設定をログに表示する
logger.log(str('\n\nSETTINGS:'))
logger.log(str(settings))
 
# 画像をウィンドウに表示
imp.show()
 
# 元画像とTrackMateのモデルを重ねて表示
displayer =  HyperStackDisplayer(model, sm, imp, ds)
displayer.render()

# ログに記述
model.getLogger().log('Found ' + str(model.getTrackModel().nTracks(True)) + ' tracks.')
 
# 対応づけ(リンク)と、追跡対象が保持している値(feature)を取得
fm = model.getFeatureModel()

# 各軌跡の先頭フレームを探すため、先頭フレームを格納するリストを先に作成する
StartFrames = [NumFrame] * len(model.getTrackModel().trackIDs(True))
StartIDs = [0] * len(model.getTrackModel().trackIDs(True))
# 解析対象としている軌跡の中で繰り返し処理を行う
for id in model.getTrackModel().trackIDs(True): 
    # 現在の軌跡の中の全ての対象(spot)に対して処理を行う
    track = model.getTrackModel().trackSpots(id)
    for spot in track:
        sid = spot.ID() # 繰り返し処理の対象としているspotのIDを得る
        t=spot.getFeature('FRAME') # 繰り返し処理の対象としているspotのフレームを得る
        t_int = int(t) # フレームは文字列で格納されていたので整数型に変換
        if t_int < StartFrames[id]: # 得られたフレームが小さければStartFramesへ更新
        	StartFrames[id] = t_int
        	StartIDs[id] = sid # 同時に小さい時のspotのIDもStartIDsに格納

model.beginUpdate()
Idx = 0
for head in StartIDs:
	if StartFrames[Idx] >0: # 元画像の先頭フレームは除外してそれ以外で処理
		HeadSpot = spots.search(head) # 先頭spot
		PartnerSpot = spots.getClosestSpot(HeadSpot,StartFrames[Idx]-1,True)
		# 先頭spotの前のフレームで距離が近いspotをPartnerSpotとする
		IID = PartnerSpot.ID()
		model.addEdge(PartnerSpot,HeadSpot,-1)	
		# 先頭とパートナーを対応づける
	Idx = Idx + 1 # 先程抽出した全ての先頭軌跡について処理する
model.endUpdate()

# 画像の表示
imp.show()
# モデルの画像への重ね描き
displayer =  HyperStackDisplayer(model, sm, imp, ds)
displayer.render()
# 軌跡の表示
trackscheme = TrackScheme(model, sm, ds)
trackscheme.render()

#ファイルを保存するパスの指定
# 適宜、自分のパス、ファイル名へ置き換えること
Outfile = File('/Users/yuki-ts/Documents/TrackMate/test.xml')
# ファイルハンドラのコンストラクタ
writer = TmXmlWriter(Outfile)
# 今回処理したモデルをファイルハンドラへ加える
writer.appendModel(model)
# 設定ファイルも加える
writer.appendSettings(settings)
# ファイルへの書き込み実施
writer.writeToFile()
