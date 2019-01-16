import cv2

def read_frame(video_file, nth_frame = 20):
	vidcap = cv2.VideoCapture(video_file);
	success,image = vidcap.read()
	count = 0
	success = True

	while success:
		success,image = vidcap.read()
		print('read a new frame:',success)
		if count % nth_frame == 0 :
			cv2.imwrite('frame%d.jpg'%count,image)
			print('success')
		count+=1
