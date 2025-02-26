from pymmcore_plus import CMMCorePlus

# MMCoreへのインターフェースを取得
mmc = CMMCorePlus.instance()
# MMConfig_demo.cfgを読み込む
mmc.loadSystemConfiguration()

# -----


mmc.setShutterOpen(True)
mmc.waitForDevice(mmc.getShutterDevice())
mmc.snap()
mmc.setShutterOpen(False)
mmc.waitForDevice(mmc.getShutterDevice())
