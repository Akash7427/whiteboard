# -*- coding: utf-8 -*-
# @Author: amish
# @Date:   2021-04-15 19:29:21
# @Last Modified by:   amish
# @Last Modified time: 2021-04-15 19:44:18

import cv2, sys, os
from modules import glob

def read_image(s):
	try:
		path = os.path.join(glob.image_path, s)
		img = cv2.imread(path)
		return img
	except:
		# print(sys.exc_info()[1])
		# print("Image Can't be loaded!!")
		return None