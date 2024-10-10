#@ Integer (Label = "Gaussian Blur (Disabled if 0)", value = 1) sigma
from ij import IJ
imp = IJ.getImage()

if sigma > 0: # sigmaが有効な数字の時のみガウスぼかしを行う
	IJ.run(imp, "Gaussian Blur...", "sigma=" + str(sigma) + " stack")
