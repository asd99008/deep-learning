import cv2 as cv
import numpy as np
import random
import argparse
import os

def crop(img,roi):
	"""
	img: 图像矩阵
	roi: 待截取的区域，格式为：(top,bottom,left,right)
	"""
	top,bottom,left,right=roi
	bottom = img.shape[0] if bottom>img.shape[0] else bottom
	right = img.shape[1] if right>img.shape[1] else right
	return img[top:bottom,left:right]
	
def color_shift(img,shift=50):
	"""
	img: 图像矩阵
	shift: 像素值偏移值
	"""
	r_offset = random.randint(-abs(shift),abs(shift))
	g_offset = random.randint(-abs(shift),abs(shift))
	b_offset = random.randint(-abs(shift),abs(shift))
	img = img+np.array([b_offset,g_offset,r_offset])
	img[img<0]=0
	img[img>255]=255
	return img
	
def rotate(img,angle=30,scale=1):
	"""
	img: 图像矩阵
	angle: 选转角度
	scale:缩放因子
	"""
	rows,cols = img.shape[:2]
	M = cv.getRotationMatrix2D((int(cols/2),int(rows/2)),angle,scale)
	img_rotate = cv.warpAffine(img,M,(cols,rows))
	return img_rotate
def perspective(img,random_margin=60):
	"""
	img: 图像矩阵
	random_margin: 随机值，用来生成坐标
	"""
	height,width = img.shape[:2]
	x1 = random.randint(-random_margin, random_margin)
	y1 = random.randint(-random_margin, random_margin)
	x2 = random.randint(width - random_margin - 1, width - 1)
	y2 = random.randint(-random_margin, random_margin)
	x3 = random.randint(width - random_margin - 1, width - 1)
	y3 = random.randint(height - random_margin - 1, height - 1)
	x4 = random.randint(-random_margin, random_margin)
	y4 = random.randint(height - random_margin - 1, height - 1)

	dx1 = random.randint(-random_margin, random_margin)
	dy1 = random.randint(-random_margin, random_margin)
	dx2 = random.randint(width - random_margin - 1, width - 1)
	dy2 = random.randint(-random_margin, random_margin)
	dx3 = random.randint(width - random_margin - 1, width - 1)
	dy3 = random.randint(height - random_margin - 1, height - 1)
	dx4 = random.randint(-random_margin, random_margin)
	dy4 = random.randint(height - random_margin - 1, height - 1)

	pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
	pts2 = np.float32([[dx1, dy1], [dx2, dy2], [dx3, dy3], [dx4, dy4]])
	M = cv.getPerspectiveTransform(pts1,pts2)
	img_pers = cv.warpPerspective(img,M,(width,height))
	return img_pers

# def perspective(img,pos1,pos2):
	# """
	# img: 图像矩阵
	# pos1: 原图像中四组坐标值, 格式为((x1,y1),(x2,y2),(x3,y3),(x4,y4))
	# pos2 投影变换后图像中四组坐标值,格式同from
	# """
	# pos1 = np.float32(pos1)
	# pos2 = np.float32(pos2)
	# M = cv.getPerspectiveTransform(pos1,pos2)
	# img_pers = cv.warpPerspective(img,M,(img.shape[1],img.shape[0]))
	# return img_pers

def argparser():
	parser = argparse.ArgumentParser()
	parser.add_argument("--img_input", type=str,help="输入图片路径")
	parser.add_argument("--img_output", type=str,help="输出图片路径")
	parser.add_argument("--roi", nargs='*',type=int,help="待截取的区域，格式为：(top,bottom,left,right)")
	parser.add_argument("--shift",type=int,help="像素值偏移值")
	parser.add_argument("--angle",type=float,help="旋转角度")
	parser.add_argument("--scale",type=float,help="缩放因子")
	parser.add_argument("--margin",type=int,help="随机值，用来生成坐标")
	
	return parser.parse_args()

if __name__=="__main__":
	parse = argparser()
	img_dir = parse.img_input
	out_dir = parse.img_output
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	if os.path.exists(img_dir):
		for file in os.listdir(img_dir):
			if file.endswith(("jpg","png")):
				img = cv.imread(os.path.join(img_dir,file))
				if parse.roi and len(parse.roi)==4:
					img = crop(img,parse.roi)
				if parse.shift:
					img = color_shift(img,parse.shift)
				if parse.angle and parse.scale:
					img = rotate(img,parse.angle,parse.scale)
				if parse.margin:
					img = perspective(img,parse.margin)
				cv.imwrite(os.path.join(out_dir,file),img)
