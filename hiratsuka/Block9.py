#@ File    (label = "Input directory", style = "directory") srcFile
#@ File    (label = "Output directory", style = "directory") dstFile
#@ String  (label = "File extension", value=".tif") ext
#@ String  (label = "File name contains", value = "") containString

import os
import sys
from ij import IJ, ImagePlus
from loci.plugins import BF
from loci.plugins.in import ImporterOptions

srcDir = srcFile.getAbsolutePath()
dstDir = dstFile.getAbsolutePath()
print srcDir
print dstDir
filecol = [] #ファイル名の集まり。はじめは空で初期化
rootcol = [] #フォルダ名の集まり。はじめは空で初期化

for root, directories, filenames in os.walk(srcDir): #指定したフォルダ内の探索
	filenames.sort() #ファイル名の並び替え
	for filename in filenames: #ファイルごとに条件のチェック
		if not filename.endswith(ext): #拡張子のチェック
			continue #条件を満たさないときはスキップ
		if containString not in filename: #ファイル名のチェック
			continue #条件を満たさないときはスキップ
		filecol.append(filename)
		rootcol.append(root)

for i in range(len(filecol)): #条件を満たすファイルについて繰り返し処理
  	print(os.path.join(rootcol[i],filecol[i])) #ファイルのパスを表示
  	#ここに処理を書くと全てのファイルに実行される
