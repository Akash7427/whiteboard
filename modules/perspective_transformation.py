# -*- coding: utf-8 -*-
# @Author: amish
# @Date:   2021-04-15 19:15:26
# @Last Modified by:   amish
# @Last Modified time: 2021-04-15 19:37:53


import cv2
from modules import four_point_transform

def perspective(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 199, 5)
	try:
		copy = thresh.copy(); orig = img.copy()
		cnts = cv2.findContours(copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if len(cnts) == 2 else cnts[1]
		area = -1; c1 = 0
		for c in cnts:
			epsilon = 0.01 * cv2.arcLength(c,True)
			approx = cv2.approxPolyDP(c,epsilon,True)
			if len(approx) == 4 and area < cv2.contourArea(c):
				area = cv2.contourArea(c)
				c1 = c; approx1 = approx
		warped = four_point_transform.four_point_transform(orig, approx1.reshape(4, 2))
		return [True, warped]
	except:
		print("Image cannot be transformed!!\n")
		return [False, None]