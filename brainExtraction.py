
import numpy as np
import pandas as pd
import cv2
from PIL import Image
import os


def slice(source, template, path, source1):
    source = cv2.cvtColor(source, cv2.COLOR_RGB2GRAY)
    template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
    Height, Width = template.shape
    methods = [cv2.TM_CCORR_NORMED]
    threshold = 0.8
    source2 = source.copy()
    result = cv2.matchTemplate(source2, template, cv2.TM_CCOEFF_NORMED)
    location = np.where(result >= threshold)
    rgb = cv2.cvtColor(source1, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(source1, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(source1, cv2.COLOR_RGB2BGR)
    i = 1
    for j in zip(location[1], location[0]):
        slice = gray[j[1] + 10:j[1] + Height +
                     110, j[0] + 10:j[0] + Width + 110]
        if cv2.countNonZero(slice) != 0:
            try:
                crop = rgb[j[1] + 10:j[1] + Height +
                           110, j[0] + 10:j[0] + Width + 110]
                cv2.imwrite(path+'/IMG-'+str(i)+'.png', crop)
                i += 1
            except:
                continue


def boundary(image, boundary_path, k):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(blurred, 10, 100)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilate = cv2.dilate(edged, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(
        dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    image = cv2.drawContours(image, contours, -1, (0, 255, 0), 1)
    cv2.imwrite(os.path.join(boundary_path, "IMG-%s.png" % k), image)
