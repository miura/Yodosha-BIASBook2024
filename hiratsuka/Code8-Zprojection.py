from ij.process import StackStatistics
from ij.plugin import ZProjector

#　ベースライン輝度の引き算の関数
def Baseline_subtraction(imp):
	imp_2D = ZProjector.run(imp,"max")
	stat_imp = StackStatistics(imp_2D)
	minVal_imp = stat_imp.min
	IJ.run(imp, "Subtract...", \
	"value=" + str(minVal_imp) + " stack")

Baseline_subtraction(imp_mCherry)
Baseline_subtraction(imp_mVenus)

