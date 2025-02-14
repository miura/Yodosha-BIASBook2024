#@ Integer (Label = "Gaussian Blur (Disabled if 0)", value = 1) sigma

#　ガウスぼかしの関数
def Gaussian_filter(imp,sigma):
	if sigma > 0:
		print "Gaussian Blur: sigma: " + str(sigma)
	IJ.run(imp, "Gaussian Blur...", \
		"sigma=" + str(sigma) + " stack")

Gaussian_filter(imp_add, sigma)
