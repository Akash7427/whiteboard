# -*- coding: utf-8 -*-
# @Author: amish
# @Date:   2021-04-15 18:56:32
# @Last Modified by:   amish
# @Last Modified time: 2021-04-15 19:57:13

from modules import perspective_transformation, read, color_correction

def main_func(filename):
	img = read.read_image(filename)
	flag, warped = perspective_transformation.perspective(img)
	if flag == False or (warped.shape[0] < 600 and warped.shape[1] < 600):
		# sys.exit("Image couldn't be transformed!!")
		return [False, None]
	else:
		sharpen_image = color_correction.simplest_cb(warped, 1)
		return [True, sharpen_image]