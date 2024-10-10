#@ Integer (label = "Background subtraction (Disabled if 0)", value = 50) BGval
from ij import IJ
imp = IJ.getImage()

if BGval >0: # BGValが有効な数字の時のみガウスぼかしを行う
	IJ.run(imp, "Subtract Background...", "rolling=" + str(BGval) + " stack")
