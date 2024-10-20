from ij.io import DirectoryChooser
import os

srcDir = DirectoryChooser("please select a folder").getDirectory()
print("directory: "+srcDir)
for root, directories, filenames in os.walk(srcDir):
	for filename in filenames:
		if filename.endswith(".tif"):
			path = os.path.join(root, filename)
			print(path)