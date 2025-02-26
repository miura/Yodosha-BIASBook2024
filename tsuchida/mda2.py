from pymmcore_plus import CMMCorePlus
from useq import MDAEvent
mmc = CMMCorePlus.instance()
mmc.loadSystemConfiguration()

# 取得画像を受けとる関数を定義し，mmcに接続
@mmc.mda.events.frameReady.connect
def on_frame(image, event):
    # imageはnumpy.ndarray，eventはMDAEvent.
    print(f"フレーム {event.index}, サイズ {image.shape}を取得")
    # ここで画像を表示・解析・保存などする.

mda_sequence = [
    # 取得画像を扱いやすいように，時間（"t"）インデックスを振る
    MDAEvent(index={"t": 0}, reset_event_timer=True),
    MDAEvent(index={"t": 1}, min_start_time=10.0),
    MDAEvent(index={"t": 2}, min_start_time=20.0),
]

mmc.run_mda(mda_sequence)
