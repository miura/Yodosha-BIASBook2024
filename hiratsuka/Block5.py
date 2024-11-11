from ij import IJ

#　ガウスぼかしの関数
def Gaussian_filter(imp,sigma):

	imp = IJ.getImage()
	IJ.run(imp, "Gaussian Blur...", \
		"sigma=" + str(sigma) + " stack");

#アクティブな画像の取得
imp = IJ.getImage()
sigma = 2
Gaussian_filter(imp, sigma)
