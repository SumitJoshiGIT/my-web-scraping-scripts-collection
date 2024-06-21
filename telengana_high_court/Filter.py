import cv2 
from PIL import Image
import numpy as np


def filter():
 img  = cv2.imread("temp.png")
 c_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
 kernel = np.ones((3,3),np.uint8)
 out = cv2.medianBlur(c_gray,3)
 
 a = np.where(out>195, 1, out)
 out = np.where(a!=1, 0, a)
 out = cv2.medianBlur(out,3)
 return Image.fromarray(out*255)