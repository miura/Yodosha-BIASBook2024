from pymmcore_plus import CMMCorePlus

# MMCoreへのインターフェースを取得
mmc = CMMCorePlus.instance()
# MMConfig_demo.cfgを読み込む
mmc.loadSystemConfiguration()
# デバイス一覧を表示
mmc.describe()


# 現在の設定で画像をスナップ
image = mmc.snap()
# 返り値はNumPy array
image.shape


# napariで取得画像を表示
import napari
napari.imshow(image)


# ---

# napariを終了するまで走らせる (対話的に使用時は不要)
napari.run()
