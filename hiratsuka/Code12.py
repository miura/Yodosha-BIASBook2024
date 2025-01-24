#@ File    (label = "Input directory", style = "directory") srcFile
#@ File    (label = "Output directory", style = "directory") dstFile
#@ String  (label = "File extension", value=".tif") ext
#@ String  (label = "File name contains", value = "") containString

import os
import sys
from ij import IJ, ImagePlus
from loci.plugins import BF
from loci.plugins.in import ImporterOptions

#ポップアップアップウインドウで取得した情報
	#探索するフォルダの絶対パスを取得
srcDir = srcFile.getAbsolutePath()
	#画像を保存するフォルダの絶対パスを取得
dstDir = dstFile.getAbsolutePath()
print srcDir + str(srcDir)
print dstDir + str(dstDir)
#ファイル名の集まり。はじめは空で初期化
filecol = [] 
#フォルダ名の集まり。はじめは空で初期化
rootcol = [] 

#指定したフォルダ内の探索
for root, directories, filenames in os.walk(srcDir): 
	#ファイル名の並び替え
	filenames.sort() 
	#ファイルごとに条件のチェック
	for filename in filenames: 
		#拡張子のチェック
		if not filename.endswith(ext): 
			#条件を満たさないときはスキップ	
			continue 
		#ファイル名のチェック
		if containString not in filename: 
			#条件を満たさないときはスキップ
			continue 
		filecol.append(filename)
		rootcol.append(root)

#条件を満たすファイルについて繰り返し処理
for i in range(len(filecol)): 
#ファイルのパスを表示  	
	print(os.path.join(rootcol[i],filecol[i])) 
  	#ここに処理を書くと全てのファイルに実行される
