#@ Integer (label = "Background subtraction (Disabled if 0)", value = 50) BGval

#　背景の引き算処理の関数
def Background_subtraction(imp,BGval):
	if BGval >0:
		print "Background subtraction: rolling ball: " \
			+ str(BGval)
		IJ.run(imp, "Subtract Background...", \
			"rolling=" + str(BGval) + " stack")

Background_subtraction(imp_add, BGval)
