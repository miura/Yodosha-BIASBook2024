from ij.plugin import Concatenator
from ij.plugin import HyperStackConverter

def concat_HSC(imp1,imp2,imp3):
	imp_dim = imp1.getDimensions()
	#Channel,Z,Tの枚数などの表示
	print(imp_dim)
	imp_concat = Concatenator.run(imp1, imp2, imp3)
	#Hyperstackへの変換
	imp_HSC = HyperStackConverter.\
	toHyperStack(imp_concat, 3, \
	imp_dim[3], imp_dim[4], \
	"xyztc", "grayscale")
	return imp_HSC

imp_HSC = concat_HSC(imp_mCherry,imp_mVenus,imp_add)
imp_HSC.show()
