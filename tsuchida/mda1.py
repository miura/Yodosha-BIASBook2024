from pymmcore_plus import CMMCorePlus
from useq import MDAEvent
mmc = CMMCorePlus.instance()
mmc.loadSystemConfiguration()  #デモを使用

# 手順を定義
mda_sequence = [
    MDAEvent(reset_event_timer=True),
    MDAEvent(min_start_time=10.0),
    MDAEvent(min_start_time=20.0),
]

# 手順を実行
mmc.run_mda(mda_sequence)
