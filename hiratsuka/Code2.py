#ブロック1に続けて書く

from ij.plugin import ImageCalculator

#インスタンスを作成
IC = ImageCalculator()

imp_add = imp_mCherry.duplicate() 
IC.run("add stack", imp_add, imp_mVenus)
#結果は複製したimp_addに上書きされる

 #結果の表示
imp_add.show()
