from pymmcore_plus import CMMCorePlus
from useq import MDAEvent
mmc = CMMCorePlus.instance()
mmc.loadSystemConfiguration()  #デモを使用

# ---


import useq

# 手順を定義
mda_sequence = useq.MDASequence(
    # 多次元座標軸の順番: 各タイムポイントでZスタック，
    # 各Zスライスで多チャネル，の順番を指定
    axis_order="tzc",
    # 60秒間隔で5回
    time_plan=useq.TIntervalLoops(interval=60.0, loops=5),
    # 現在位置の上下7.5 μmの範囲を3 μm間隔で
    z_plan=useq.ZAboveBelow(above=7.5, below=7.5, step=3.0),
    # 設定グループ"Channel"のプリセット"DAPI","FITC"を
    # チャネルとして使用，露光時間はそれぞれ30 ms,100 ms
    channels=(
    useq.Channel(group="Channel", config="DAPI", exposure=30.0),
    useq.Channel(group="Channel", config="FITC", exposure=100.0),
    ),
)

# 手順を実行
mmc.run_mda(mda_sequence)
