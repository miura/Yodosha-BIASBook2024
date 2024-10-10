sigma = 2
from ij import IJ
imp = IJ.getImage()
IJ.run(imp, "Gaussian Blur...", "sigma=" + str(sigma) + " stack"); #文字列の結合
#最後のセミコロンはなくても良い
