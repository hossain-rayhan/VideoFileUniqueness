import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import random
import math
import csv


K=4		#default K value
MaxI=800	#default limit on iterations
MVThresh = 0.099	#movement threshold
NPCA = 2	#number of PCAs to look through

#class used to organize data by cluster
class Cluster:
	def __init__(self, num, x, y):
		self.Num = num
		self.X = x	#x-center of the cluster
		self.Y = y	#y-center of the cluster
		self.MoveF = 0	#movement is allowed
		self.frames = []

	def addFrame(self, F):
		self.frames.append(F)
	def getNo(self):
		return self.Num

	def setF(self, x):
		self.MoveF = x
	def getF(self):
		return self.MoveF

	def setX(self, x):
		self.X = x
	def getX(self):
		return self.X

	def setY(self, y):
		self.Y = y
	def getY(self):
		return self.Y

	def printC(self):
		print("%d\t%d\t%f\t%f" %(self.Num, self.MoveF, self.X, self.Y))
		for f in self.frames:
			f.printS()

#class to hold frame data
class Frame:
	def __init__(self, fNo, x, y):
		self.FNo = fNo
		self.X = x	#x value of the corresponding PCA
		self.Y = y	#y value of the corresponding PCA
#		self.Frame = Fr.copy();	#have the frame on hand if necessary
		self.clusterNo = -1
	def setCluster(self, A):
		self.clusterNo = A
	def getCluster(self):
		return self.clusterNo
	def getName(self):
		return self.name

	def getX(self):
		return self.X
	def getY(self):
		return self.Y

	def printS(self):
		print("--%5d %5.4f %5.4f" %(self.FNo, self.X, self.Y))


def getData(str):
	data = []
	with open(str) as CSV_:
		d = csv.reader(CSV_, delimiter=',')
		for i, row in enumerate(d):
			if(i!=0):
				for index, R in enumerate(row):
					try:
						row[index] = float(R)
					except:
						continue
				data.append(row)
			#	print(row)
	return data

def Dis(clu, S):
	#return the distance of the cluster and the Frame
	return (math.sqrt((clu.getX() - S.getX())**2+(clu.getY() - S.getY())**2))

def Mindex(D):
	#return the minimum index of a distance
	A = math.inf
	out = 0
	for index, i in enumerate(D):
		if(i < A):
			A = i
			out = index
	return out

def Kmeans(clusters, Frames, itter):
	if(itter == MaxI):	#safety net
		return itter
	tmp = []
	#figure out where each school clusters to
	for c in clusters:
		c.frames.clear()
	for F in Frames:
		for c in clusters:
			tmp.append(Dis(c, F))
		clusters[Mindex(tmp)].addFrame(F)
		tmp.clear()

	Xavg = 0
	Yavg = 0
	MV = 0
	#set the position of the cluster to the average of the schools closest to it
	for index, c in enumerate(clusters):
		if(clusters[index].getF() != 1):
			#get the average
			for F in c.frames:
				Xavg += F.getX()
				Yavg += F.getY()
			#find if the cluster has no frames
			oldX = c.getX()
			oldY = c.getY()
			if(len(c.frames) != 0 and itter != MaxI):
				c.setX(Xavg/len(c.frames))
				c.setY(Yavg/len(c.frames))
			else:
				continue
#				print("cluster %d has no nearby frames in itteration %d" %(c.Num, itter))

			if((len(c.frames)!= 0) and (math.sqrt((oldX - Xavg/len(c.frames))**2+(oldY - Yavg/len(c.frames))**2) < MVThresh)):
				clusters[index].setF(1)
				MV+=1
		else:
			MV+=1
			if(MV == K):
				#print("HI")
				return itter

	A = Kmeans(clusters, Frames, itter+1)
	Bframes = []
	if(itter == 0):
		for c in clusters:
			if(len(c.frames) != 0):
				Bframes.append(nearestF(c))
	return A, Bframes

def nearestF(cluster):
	D = math.inf
	out = 0;
	for F in cluster.frames:
		if(Dis(cluster, F) < D):
			D=Dis(cluster, F)
			out = F
	return out

def MaxDist(Frames, FNO, used):
	max = -1.0		#distance var
	max1 =-1		#point index
	tmp = 0.0

	for x in range(0, len(Frames)):
		tmp = 0.0
		for y in range(0, len(Frames)):
			if(used[x]==0 and used[y]==0):
				if(FNO[x]!= FNO[y]):
					tmp+=Dis(Frames[x], Frames[y])
		if(tmp > max):	#new maximum sum of distances
			max = tmp
			max1 = x

	return max1

def getBframes(arr):
	out = []
	out1 = []
	out2 = []
	out3 =[]
	out4 = []
	for index, a in enumerate(arr):
		out4.append(-1)
		for i2, b in enumerate(a):
			out.append(b)
			out1.append(index)
			out2.append(i2)
			out3.append(0)
	return out, out1, out2, out3, out4


def PicVframes(VidF):	#takes in the list of best frames organized by vid# returns INDEXES OF BEST FRAMES
	Tracker = VidF.copy()	#poped from to rebuild cluster W/O decided video
	Frames, INDS, Vind, used, out = getBframes(VidF)
	numVids = len(VidF)

	for f in Frames:
		print(f)
	U, SIG, VT= np.linalg.svd(Frames, full_matrices=True)

	P1 = U[0].copy()
	P2 = U[1].copy()

	F = []
	flag = 0
	for index, P in enumerate(P1):
		A = Frame(index, P1[index], P2[index])
		F.append(A)
	while(numVids != 0):	#while we still have videos
		flag =0
		index = MaxDist(F, Vind, used)	#find the largest sum of distances
		V = INDS[index]
		ind = Vind[index]
		out[V] = ind
		i=0
		while(i < len(F)):

			if(INDS[i] == V):
				flag = 1
				F.pop(i)
				Vind.pop(i)
				INDS.pop(i)
				used.pop(i)
			else:
				if(flag == 1):
					break
				i+=1
		numVids-=1
#	print(out)
	return out
#TEST = [[[26, 150, 18, 98, 95, 1, 65, 28, 19, 119, 3, 27, 116, 16, 161, 43247.234, -10125.043, -10125.043, -8708.595, 7186.96, 0, -3495.2795, 3495.2795, -3295.5518, -1038.7915], [145, 21, 87, 95, 18, 61, 0, 11, 119, 28, 26, 3, 14, 161, 116, 43247.234, -10125.043, -10125.043, -8708.595, 7186.96, 0, -3495.2795, 3495.2795, -3295.5518, -1038.7915]], [[6, 51, 110, 104, 25, 13, 71, 25, 138, 39, 14, 92, 18, 169, 53, 65993.164, 9623.668, 9623.667, -6078.827, 4060.6895, 0, -563.89417, 563.89417, -1344.2504, 4718.924],  [31, 59, 8, 113, 111, 47, 80, 17, 151, 24, 62, 105, 19, 180, 17, 65993.164, 9623.668, 9623.667, -6078.827, 4060.6895, 0, -563.89417, 563.89417, -1344.2504, 4718.924]]]
#TEST = [[[107, 3, 208, 135, 32, 82, 5, 208, 119, 167, 72, 5, 208, 113, 230, 129714.59, -12416.072, -12416.072, -10086.683, -10086.683, 0, -3671.425, 3671.4248, -5494.782, 5494.782], [134, 3, 32, 106, 208, 118, 5, 167, 81, 208, 111, 4, 230, 71, 208, 129714.59, -12416.072, -12416.072, -10086.683, -10086.683, 0, -3671.425, 3671.4248, -5494.782, 5494.782], [3, 32, 207, 133, 105, 5, 167, 207, 117, 80, 4, 230, 207, 110, 70, 129714.59, -12416.072, -12416.072, -10086.683, -10086.683, 0, -3671.425, 3671.4248, -5494.782, 5494.782]], [[18, 82, 143, 19, 94, 28, 9, 60, 0, 119, 116, 13, 26, 2, 161, 43247.234, -10125.043, -10125.043, -8708.595, 7186.96, 0, -3495.2795, 3495.2795, -3295.5518, -1038.7915], [94, 18, 80, 142, 18, 119, 1, 8, 59, 28, 161, 2, 12, 25, 116, 43247.234, -10125.043, -10125.043, -8708.595, 7186.96, 0, -3495.2795, 3495.2795, -3295.5518, -1038.7915], [70, 95, 18, 139, 13, 4, 119, 28, 56, 1, 10, 161, 116, 25, 2, 43247.234, -10125.043, -10125.043, -8708.595, 7186.96, 0, -3495.2795, 3495.2795, -3295.5518, -1038.7915]], [[110, 33, 9, 65, 131, 33, 50, 17, 89, 172, 25, 67, 20, 118, 192, 65993.164, 9623.668, 9623.667, -6078.827, 4060.6895, 0, -563.89417, 563.89417, -1344.2504, 4718.924], [14, 48, 136, 56, 109, 25, 66, 161, 102, 25, 32, 84, 176, 157, 18, 65993.164, 9623.668, 9623.667, -6078.827, 4060.6895, 0, -563.89417, 563.89417, -1344.2504, 4718.924], [31, 59, 8, 113, 111, 47, 80, 17, 151, 24, 62, 105, 19, 180, 17, 65993.164, 9623.668, 9623.667, -6078.827, 4060.6895, 0, -563.89417, 563.89417, -1344.2504, 4718.924]]]
#PicVframes(TEST)

def PlotD(Sch, clus):
	plt.figure()
	col = ['bo','go','ro','co','mo','yo','ko']
	Ccol = ['b+','g+','r+','c+','m+','y+','k+']
	X = []
	Y = []
	i=0
	for c in clus:
		for S in c.frames:
			X.append(S.getX())
			Y.append(S.getY())
		plt.plot(X,Y, col[i%len(col)])
		plt.plot(c.getX(), c.getY(), Ccol[i%len(Ccol)])
		X.clear()
		Y.clear()
		i+=1
	legend = 'K value = %d'%(K)
	leg = plt.legend([legend], loc='best', borderpad=0.3,
		shadow=False, prop=matplotlib.font_manager.FontProperties(size='small'),
		markerscale=0.4)
	leg.get_frame().set_alpha(0.4)
	plt.ylabel("pca1")
	plt.xlabel("pca2")
	#outF = sys.argv[2] + ".png"
	outF = "trainpicture.png"
	plt.savefig(outF)
	plt.close()
def Transpose(data):

        TOT = len(data[0])
        RES = []
        temp = []
        for x in range(TOT):
                temp.clear()
                for index, line in enumerate(data):
                        try:
                                temp.append(float(line[x]))
                        except:
                                temp.append(line[x])
                RES.append(temp.copy())
        return RES


def CLUSTER(d): #pixel data comes in in 2d vector, only way to do svd

	#perform svd, need to decide on some issues
	U, SIG, VT= np.linalg.svd(d, full_matrices=True)

#	VT = Transpose(VT)
	P1 = U[0].copy()
	P2 = U[1].copy()
#	print("U  - %d by %d" %(len(U[0]), len(U)) )
#	print("VT - %d by %d" %(len(VT[0]), len(VT)) )
	data = []
	for index, P in enumerate(P1):
		A = Frame(index, P1[index], P2[index])
		data.append(A)
		#A.printS()
	ra = []
	#select K random frames for K-means
	for x in range(K):
		ra.append(random.randint(0, len(data)-1))
	clu = []
	#set up initial cluster based on the random frames
	for x in range(0, K):
		A = Cluster(x, data[ra[x]].getX(), data[ra[x]].getY())
		clu.append(A)
	OUT, FR = Kmeans(clu, data, 0)

	bestframesout = []
	for f in FR:
		bestframesout.append(f.FNo)

	PlotD(data, clu)

	return bestframesout

#D = getData(sys.argv[1])
#CLUSTER(D)
