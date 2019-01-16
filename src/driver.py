########################################
# Project: Video File Uniqueness
# Professor: Dr. Audris Mockus
########################################

import argparse
import pandas as pd
import cv2 
from quantzxn import *
from geom import *
from storage import *
from read_frame import *
from write_frame import *
from Kmeans import *
import glob

## Parse the arguments.
parse = argparse.ArgumentParser()
parse.add_argument("data_path", help="Absolute path of directory containing the raw data.")
parsedargs = parse.parse_args()

## Check for errors in the command-line arguments.
path = parsedargs.data_path

## Generate list of strings of video file names using glob or subprocess.
data = glob.glob(path + "/*.avi")

## Instantiate the database.
fname = file_creation()
dbref = connectDB(fname)

## Go through videos, go through frames, store the data.
allcands = []
backtrack = []
nth_frame = 20
for i in range(len(data)):
	## Add video to DB.
	vidno = addDB_Vid(dbref, data[i])
	
	## Go through each frame per video.
	vidcap = cv2.VideoCapture(data[i])
	count = 0
	success = True

	## Parse features from the frame contents.
	while success:
		success,frm = vidcap.read()
		print('read a new frame:',success)
		if count % nth_frame == 0 :
			(rs,gs,bs) = quantize_image(frm, 5)
			(res, ims) = top5geo(frm)
			fidno = addDB_Frame(dbref, vidno, str(0), rs, gs, bs, res, ims)	
			
			print('success')
		count+=1

	## Find the thumbnail candidates for each video.
	summary = get_Frames(dbref, vidno)

	framatrix = []
	for i in range(len(summary)):
		framatrix.append([])
		for j in range(3,len(summary[i])):
			framatrix[len(framatrix)-1].append(summary[i][j])

	candidates = CLUSTER(framatrix)
	backtrack.append(candidates)

	## Store the candidates for each video.
	candmatrix = []
	for item in candidates:
		candmatrix.append([])
		dat = summary[item]
		for j in range(3,len(dat)):
			candmatrix[len(candmatrix)-1].append(dat[j])
	allcands.append(candmatrix)

## Choose the final thumbnails.
print("\n")
results=PicVframes(allcands)

## Display the final results to the user.
for i in range(len(results)):
	print("The thumbnail for video " + str(data[i]) + " is frame " + str(backtrack[i][results[i]]) + " saved in " + str(data[i]) + "_thumbnail.jpg\n")
	write_frame(data[i], backtrack[i][results[i]])
