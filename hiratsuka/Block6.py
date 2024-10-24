sigma = 2
from ij import IJ
imp = IJ.getImage()
#文字列の結合によりsigmaの値を組み込む
IJ.run(imp, \
      "Gaussian Blur...", "sigma=" + str(sigma) + " stack");
#最後のセミコロンはなくても良い