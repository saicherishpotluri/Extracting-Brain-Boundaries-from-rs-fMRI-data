import os
import shutil
import csv
from clustering import readImages

def getFiles(path):
	isDirectory = os.path.isdir(os.path.join(os.getcwd(),"Slices"))
	if isDirectory:
		shutil.rmtree(os.path.join(os.getcwd(),"Slices"))
	isDirectory = os.path.isdir(os.path.join(os.getcwd(),"Clusters"))
	if isDirectory:
		shutil.rmtree(os.path.join(os.getcwd(),"Clusters"))
	for file in os.listdir(os.path.join(path,"testPatient")):
		if "thresh" in file:
			isDirectory = os.path.isdir(os.path.join(os.getcwd(),"Slices"))
			if not isDirectory:
				os.mkdir(os.path.join(os.getcwd(),"Slices"))
			isDirectory = os.path.isdir(os.path.join(os.path.join(os.getcwd(),"Slices"),file.split('.')[0]))
			if not isDirectory:
				os.mkdir(os.path.join(os.path.join(os.getcwd(),"Slices"),file.split('.')[0]))
			isDirectory = os.path.isdir(os.path.join(os.getcwd(),"Clusters"))
			if not isDirectory:
				os.mkdir(os.path.join(os.getcwd(),"Clusters"))
			isDirectory = os.path.isdir(os.path.join(os.path.join(os.getcwd(),"Clusters"),file.split('.')[0]))
			if not isDirectory:
				os.mkdir(os.path.join(os.path.join(os.getcwd(),"Clusters"),file.split('.')[0]))
				fp = open(os.path.join(os.getcwd(),"Clusters",file.split('.')[0],file.split('.')[0]+str('.csv')),'w')
				writeToCsv = csv.writer(fp)
				writeToCsv.writerow(["Slice Number","count"])
				fp.close()
			readImages(os.path.join(path,"testPatient"),file)
	print("Execution Completed")
path = os.getcwd()
getFiles(path)
