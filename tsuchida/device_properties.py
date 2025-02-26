from pymmcore_plus import CMMCorePlus

# MMCoreへのインターフェースを取得
mmc = CMMCorePlus.instance()
# MMConfig_demo.cfgを読み込む
mmc.loadSystemConfiguration()

# -----


# デバイス・ラベル一覧を見る
mmc.getLoadedDevices()


# ラベルが"Camera"のデバイスを取得
cam = mmc.getDeviceObject("Camera")
# デバイスのプロパティ一覧を見る
cam.propertyNames()


# プロパティ"Binning"を取得
binning = cam.getPropertyObject("Binning")
# "Binning"の値を取得・変更
binning.value
binning.value = 2
# （カメラのビニングが変更されたため，画像のサイズが半分になる）
image = mmc.snap()
image.shape
