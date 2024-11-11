from ij import IJ
#アクティブな画像の取得
imp = IJ.getImage()
IJ.run(imp, "Gaussian Blur...", "sigma=2 stack"); 
#最後のセミコロンはなくても良い
