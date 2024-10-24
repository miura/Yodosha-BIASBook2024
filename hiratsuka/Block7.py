#@ Integer (Label = "Gaussian Blur (Disabled if 0)", value = 1) sigma
from ij import IJ
imp = IJ.getImage()
# sigmaが有効な数字の時のみガウスぼかしを行う
if sigma > 0: 	IJ.run(imp, \
         "Gaussian Blur...", "sigma=" + str(sigma) + " stack")