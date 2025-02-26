from pymmcore_plus import CMMCorePlus

# MMCoreへのインターフェースを取得
mmc = CMMCorePlus.instance()
# MMConfig_demo.cfgを読み込む
mmc.loadSystemConfiguration()

# -----


# 現在のカメラの露光時間を取得
mmc.getExposure()


# 露光時間を設定
mmc.setExposure(100.0) # 単位はms


# 現在のフォーカス(Z)ステージの位置を取得
mmc.getPosition()


# 位置を変更
mmc.setPosition(100.0) # 単位はμm
