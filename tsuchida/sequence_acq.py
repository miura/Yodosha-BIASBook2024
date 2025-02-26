from pymmcore_plus import CMMCorePlus

# MMCoreへのインターフェースを取得
mmc = CMMCorePlus.instance()
# MMConfig_demo.cfgを読み込む
mmc.loadSystemConfiguration()

# -----


import time

def acquire_seq(n_frames, polling_interval_ms=10):
    frames = []
    # シークエンス取得を開始，フレーム数n_frames
    # 2番目の引数は不使用（常に0.0を指定）
    # 3番目の引数はバッファ満杯時に停止するか（Trueを推奨）
    mmc.startSequenceAcquisition(n_frames, 0.0, True)
    # 取得継続中，もしくは未取り出しの画像がバッファにある間ループ
    while mmc.isSequenceRunning() or mmc.getRemainingImageCount() > 0:
        if mmc.getRemainingImageCount() > 0:
            # 次の画像をとり出し保管
            frames.append(mmc.popNextImage())
        else:
            # バッファが空（次の画像の取得待ち）の場合，しばらく待つ
            time.sleep(polling_interval_ms / 1000.0)
    mmc.stopSequenceAcquisition()
    return frames

# 10フレームのシークエンス取得
images = acquire_seq(10)
len(images)


images[0].shape
