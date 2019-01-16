import cv2

def write_frame(video_file, nth_frame):
	vidcap = cv2.VideoCapture(video_file);
	success,image = vidcap.read()
	count = 0

	success,image = vidcap.read()
	
	while (count != nth_frame):
		success,image = vidcap.read()
		count+=1
	
	cv2.imwrite(video_file+'_thumbnail.jpg',image)
