
import numpy as np
import pandas as pd
import cv2
from PIL import Image
import os
from brainExtraction import slice, boundary


data_path = os.path.abspath(os.getcwd()) + '/Data'


template_image_path = os.path.abspath(os.getcwd()) + '/template.png'


save_path = os.path.abspath(os.getcwd()) + '/'


slices = "Slices"
boundaries = "Boundaries"
counter = 0
slice_path = os.path.join(save_path, slices+'/')
boundary_path = os.path.join(save_path, boundaries+'/')


for image in os.listdir(data_path):
    if (image.endswith("_thresh.png")):
        counter += 1

if not os.path.exists(save_path+slices):
    os.makedirs(save_path+slices)
path = os.path.join(save_path, slices+'/')
for i in range(1, counter+1):
    os.mkdir(path+str(i))

if not os.path.exists(save_path+boundaries):
    os.makedirs(save_path+boundaries)
path1 = os.path.join(save_path, boundaries+'/')
for i in range(1, counter+1):
    os.mkdir(path1+str(i))


template = cv2.imread(template_image_path)
slice_path = os.path.join(save_path, slices+'/')


for x in range(1, counter+1):
    slice_images_path = data_path+'/IC_' + str(x) + "_thresh.png"
    source = cv2.imread(slice_images_path)
    source1 = cv2.imread(slice_images_path)
    template = cv2.imread(template_image_path)
    slice(source, template, slice_path+str(x), source1)


for j in range(1, counter+1):
    k = 1
    for y in range(1, len(next(os.walk(slice_path+str(j)+'/'))[2])):
        boundary_image_path = slice_path+str(j)+'/IMG-'+str(y)+'.png'
        image = cv2.imread(boundary_image_path)
        boundary(image, boundary_path+str(j), k)
        k += 1

print("Completed Execution.")
print()
