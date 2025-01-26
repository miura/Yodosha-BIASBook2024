from sc.fiji.skeletonize3D import Skeletonize3D_

def skeletonize3D( filteredlabeledimp ):
	skelimp = filteredlabeledimp.duplicate()
	skz = Skeletonize3D_()
	skz.setup("", skelimp)
	skz.run(None)
	return skelimp
	
skelimp = skeletonize3D( filteredlabeledimp )
skelimp.setTitle("BloodVessels_small_Skel.tif")
skelimp.show()