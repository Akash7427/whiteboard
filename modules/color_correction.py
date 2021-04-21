# -*- coding: utf-8 -*-
# @Author: amish
# @Date:   2021-04-15 19:17:06
# @Last Modified by:   Amish Sharma
# @Last Modified time: 2021-04-19 18:01:34

import cv2, math
import numpy as np

def apply_mask(matrix, mask, fill_value):
	masked = np.ma.array(matrix, mask=mask, fill_value=fill_value)
	return masked.filled()

def apply_threshold(matrix, low_value, high_value):
	low_mask = matrix < low_value
	matrix = apply_mask(matrix, low_mask, low_value)
	high_mask = matrix > high_value
	matrix = apply_mask(matrix, high_mask, high_value)
	return matrix

def sharpen(image):
	blur = cv2.GaussianBlur(image, (0, 0), 3)
	sharpen_image = cv2.addWeighted(image, 2.20, blur, -1, 0)
	return sharpen_image

def simplest_cb(img, percent):
	assert img.shape[2] == 3
	assert percent > 0 and percent < 100
	half_percent = percent / 200.0
	channels = cv2.split(img)
	out_channels = []
	for channel in channels:
		assert len(channel.shape) == 2
		height, width = channel.shape
		vec_size = width * height
		flat = channel.reshape(vec_size)
		assert len(flat.shape) == 1
		flat = np.sort(flat)
		n_cols = flat.shape[0]
		low_val  = flat[math.floor(n_cols * half_percent)]
		high_val = flat[math.ceil( n_cols * (1.0 - half_percent))]
		thresholded = apply_threshold(channel, low_val, high_val)
		normalized = cv2.normalize(thresholded, thresholded.copy(), 0, 255, cv2.NORM_MINMAX)
		out_channels.append(normalized)
	color_correct = cv2.merge(out_channels)
	sharpen_image = sharpen(color_correct)
	return sharpen_image