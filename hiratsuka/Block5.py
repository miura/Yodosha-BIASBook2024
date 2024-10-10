from ij import IJ
imp = IJ.getImage() #アクティブな画像の取得
IJ.run(imp, "Gaussian Blur...", "sigma=2 stack"); #最後のセミコロンはなくても良い
