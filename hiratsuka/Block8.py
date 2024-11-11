from ij.process import StackStatistics

#　ベースライン輝度の引き算の関数
def Baseline_subtraction(imp):
	stat_imp = StackStatistics(imp)
	minVal_imp = stat_imp.min
	IJ.run(imp, "Subtract...", \
	"value=" + str(minVal_imp) + " stack")

Baseline_subtraction(imp_mCherry)
Baseline_subtraction(imp_mVenus)

