import csv
import sklearn.cluster as cluster 
import numpy as np
import os
import cv2

def clusteringAndDbscan(fileName,pathOfImage,ind,csvFile):
	image = cv2.imread(os.path.join(pathOfImage,str(ind)+".png"))
	bgr2Hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	removeNoise = cv2.inRange(bgr2Hsv, (0, 0, 0), (0, 0, 255))
	extractedImage = cv2.imread(os.path.join(pathOfImage,str(ind)+".png"))
	extractedImage[np.where(removeNoise)] = 0
	grayArea = cv2.cvtColor(extractedImage,cv2.COLOR_BGR2GRAY)
	(_,threshold)=cv2.threshold(grayArea, 1, 255,cv2.THRESH_BINARY)
	(cnts, _) = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	extractedImage = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)
	extractedImage[np.where(threshold)] = [255,255,0]
	cv2.imwrite(os.path.join(os.path.join(os.getcwd(),"Clusters"),fileName.split('.')[0])+'/'+str(ind) +'.png', extractedImage)	
	counts = 0
	if(len(cnts)>0):	
		grayArea = cv2.cvtColor(extractedImage, cv2.COLOR_RGB2GRAY)
		height, width = grayArea.shape
		pointsList = []
		for i in range(0,height):
			for j in range(0,width):
				if(grayArea[i,j]>0):
					pointsList.append([i,j])
		dbScanCluster = cluster.DBSCAN(eps = 2.5,min_samples=5,n_jobs=100).fit(pointsList)
		labels, countOfLabels = np.unique(dbScanCluster.labels_[dbScanCluster.labels_>=0], return_counts=True)
		count= 0
		for size in countOfLabels:
			if(size>135):
				count = count+1
		counts = count
	else:
		counts = 0
	fp = open(csvFile,'a')
	writeToCSV = csv.writer(fp)
	writeToCSV.writerow([ind,counts])
	fp.close()


def readImages(imgPath,fileName):
	img = cv2.imread(os.path.join(imgPath,fileName))
	grayArea=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	thresholdValue=cv2.inRange(grayArea,245,255)
	edge = cv2.Canny(thresholdValue, 255, 255)
	(contours, _) = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	croppingImage(contours, fileName,imgPath)

def croppingImage(contours,fileName,imgPath):
	length=len(contours)
	ind=0
	a1,b1,c1,d1 = cv2.boundingRect(contours[length-1])
	i=0
	while i < length:
		a2,b2,c1,d1 = cv2.boundingRect(contours[length-i-1])
		if b2 != b1 and abs(b2-b1) > d1:
			break
		i = i+1
	i = 0
	while i < length:
		a3, b3, c1, d1 = cv2.boundingRect(contours[length-i-1])
		if a3 != a1 and abs(a3-a1) > c1:
			break
		i = i+1
	aLimit,bLimit,c1,d1 = cv2.boundingRect(contours[-1])
	sliceWidth =  a3-a2
	sliceHeight = b2-b1
	image = cv2.imread(os.path.join(imgPath,fileName))
	for i in range(0,length):
		count = contours[length - i -1]
		a1, b1, c1, d1 = cv2.boundingRect(count)
		a2 = a1+sliceWidth-c1
		b2 = b1-sliceHeight
		a1 = a1 + c1+c1
		b1 = b1 + d1
		if a1 < aLimit or b2 <= bLimit:
			continue
		extractedImage = image[b2:b1, a1:a2]
		grayArea =cv2.cvtColor(extractedImage,cv2.COLOR_BGR2GRAY)
		thresholdValue=cv2.inRange(grayArea,0,25)
		edge = cv2.Canny(thresholdValue, 50, 100)
		(countours, _) = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		if(len(countours)):
			finalImage = image[b2:b1, a1:a2]
			cv2.imwrite(os.path.join(os.path.join(os.getcwd(),"Slices"),fileName.split('.')[0])+'/'+str(ind) +'.png', finalImage)
			clusteringAndDbscan(fileName,os.path.join(os.getcwd(),"Slices",fileName.split('.')[0]),ind,os.path.join(os.path.join(os.getcwd(),"Clusters",fileName.split('.')[0]),fileName.split('.')[0]+'.csv'))
		ind = ind + 1

