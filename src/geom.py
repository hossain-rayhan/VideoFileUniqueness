import cv2
import numpy as np

def top5geo(img):

	## Convert frame to one channel and compute the frequency spectrum.
	img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = img2

	img = np.float32(img)/255.0
	outimg = img

	out = cv2.dft(img, outimg, cv2.DFT_COMPLEX_OUTPUT, 0)

	# Find the largest five values.
	index_i = [0, 0, 0, 0, 0]
	index_j = [0, 0, 0, 0, 0]
	value = [0, 0, 0, 0, 0]
	reals = [0, 0, 0, 0, 0]
	imags = [0, 0, 0, 0, 0]
	for i in range(len(out)):
		for j in range(len(out[0])):
			m = outimg[i][j]
			for k in range(len(index_i)):
				if m > value[k]:
					#print("Found: " + str(i) + " " + str(j))
					value[k] = m
					reals[k] = out[i][j][0]
					imags[k] = out[i][j][1]
					index_i[k] = i
					index_j[k] = j
					break
	
	return (reals, imags)
