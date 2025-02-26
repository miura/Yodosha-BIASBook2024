from pymmcore_plus import CMMCorePlus

# MMCoreへのインターフェースを取得
mmc = CMMCorePlus.instance()
# MMConfig_demo.cfgを読み込む
mmc.loadSystemConfiguration()

# -----


# （現在の）XYステージに対し...
xy = mmc.getDeviceObject(mmc.getXYStageDevice())
# 現在位置を取得
mmc.getXYPosition(xy.label)


# 相対位置を設定（=動作を開始;単位はμm）後，ただちにビジー状態を確認
mmc.setRelativeXYPosition(xy.label, 100.0, -200.0); xy.isBusy()


# XYステージがすべての動作を完了するまで待機
xy.wait()
# 待機後はビジー状態が解除されている
xy.isBusy()
