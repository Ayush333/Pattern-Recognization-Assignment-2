import matplotlib.pyplot as plt
import random
import sys
import math
from mpmath import mpf, mpc, mp



CLASS_SIZE=500
TrainingSize=375
K=32
D=2

def readDataSetTraining(fileName):
	f = open(fileName,"r")
	fl =f.readlines()[0:TrainingSize]
	dSet = [[0 for x in range(D)] for y in range(TrainingSize)] # vector which consist of 2 features;
	i=0
	for lines in fl:
		lines=lines.split();
		for j in range(D):
			dSet[i][j] = (lines[j])
		i=i+1
	f.close()
	return dSet

def readDataSetWhole(fileName):
	f = open(fileName,"r")
	fl =f.readlines()[0:CLASS_SIZE]
	dSet = [[0 for x in range(D)] for y in range(CLASS_SIZE)] # vector which consist of 2 features;
	i=0
	for lines in fl:
		lines=lines.split();
		for j in range(D):
			dSet[i][j] = float(lines[j])
		i=i+1
	f.close()
	return dSet

def getRange():
	X1=readDataSetWhole("Class1.txt")
	X2=readDataSetWhole("Class2.txt")
	X3=readDataSetWhole("Class3.txt")

	xmin=ymin=sys.maxsize
	xmax=ymax=-sys.maxsize

	for i in range(CLASS_SIZE):
		if X1[i][0] > xmax :
			xmax=X1[i][0]
		if X2[i][0] > xmax :    
			xmax=X2[i][0]
		if X3[i][0] > xmax :    
			xmax=X3[i][0]
		if X1[i][0] < xmin :    
			xmin=X1[i][0]
		if X2[i][0] < xmin :    
			xmin=X2[i][0]
		if X3[i][0] < xmin :    
			xmin=X3[i][0]

		if X1[i][1] > ymax :
			ymax=X1[i][1]
		if X2[i][1] > ymax :
			ymax=X2[i][1]
		if X3[i][1] > ymax :
			ymax=X3[i][1]
		if X1[i][1] < ymin :    
			ymin=X1[i][1]
		if X2[i][1] < ymin :    
			ymin=X2[i][1]
		if X3[i][1] < ymin :    
			ymin=X3[i][1]
	dSet = [[0 for x in range(2)] for y in range(2)]
	dSet[0][0]=xmin
	dSet[0][1]=xmax
	dSet[1][0]=ymin
	dSet[1][1]=ymax
	return dSet

def inverseMatrix(cov_matrix_b):
	det = (cov_matrix_b[0][0]*cov_matrix_b[1][1]) - (cov_matrix_b[0][1]*cov_matrix_b[1][0])
	inv_matrix=[[0 for i in range(2)]for j in range(2)]
	inv_matrix[0][1] = -1*cov_matrix_b[0][1]
	inv_matrix[1][0] = -1*cov_matrix_b[1][0]
 
	inv_matrix[0][0] = cov_matrix_b[1][1]
	inv_matrix[1][1] = cov_matrix_b[0][0];

	for i in range(D):
		for j in range(D):
			inv_matrix[i][j] /= det;
	return inv_matrix

def calcDet(matrix):
	det = (matrix[0][0]*matrix[1][1]) - (matrix[0][1]*matrix[1][0])        
	return det

def Distribution(x,Sigma,Mean):
	# print("Sigma = ",Sigma)
	SigmaInverse=inverseMatrix(Sigma)
	# print("SigmaInverse = ",SigmaInverse)
	# print("x = ",x)
	# print("Mean = ",Mean)	
	mean=[0 for i in range(D)]
	for i in range(D):
		mean[i]=x[i]-Mean[i]
	# print("mean=",mean)
	t=[((mean[0]*SigmaInverse[0][0])+(mean[1]*SigmaInverse[1][0])), ((mean[0]*SigmaInverse[0][1])+(mean[1]*SigmaInverse[1][1]))]
	w0=((t[0]*mean[0])+(t[1]*mean[1]))/2
	# print("w0pehle=",w0)
	w0=-w0
	# print("w0=",w0)
	w0=(math.exp(w0))
	# print("w0 after exp",w0)
	w0/=(pow(2*math.pi,D/2)*pow(calcDet(Sigma),0.5))
	# print(w0)
	return (w0)

def calcG(Pi,clusterCentres,Sigma,x):
	ans=0
	for i in range(K):
		ans+=Pi[i]*Distribution(x,Sigma[i],clusterCentres[i])
	# ans=math.log(ans)
	return ans

def main():
	#Allocating Memory
	Pi1=[0 for x in range(K)]
	Pi2=[0 for x in range(K)]
	Pi3=[0 for x in range(K)]
	
	clusterCentres1=[[0 for x in range(D)]for y in range(K)]
	clusterCentres2=[[0 for x in range(D)]for y in range(K)]
	clusterCentres3=[[0 for x in range(D)]for y in range(K)]
	
	Sigma1=[[[0 for x in range(D)]for y in range(D)]for z in range(K)]
	Sigma2=[[[0 for x in range(D)]for y in range(D)]for z in range(K)]
	Sigma3=[[[0 for x in range(D)]for y in range(D)]for z in range(K)]
	
	#Reading Class 1
	f=open("32/Class1afterGMM.txt","r")
	#Filling means of clusters of class1
	for i in range(K):
		line=next(f)
		line=line.split()
		for j in range(D):
			clusterCentres1[i][j]=float(line[j])
		print(clusterCentres1[i])
	#Filling Sigma of clusters of class1
	for i in range(K):
		line=next(f)
		line=line.split()
		for j in range(D):
			for k in range(D):
				Sigma1[i][j][k]=float(line[(j*2)+(k*1)])
		print(Sigma1[i])
	#Filling Pi of clusters of class1
	for i in range(K):
		line=next(f)
		Pi1[i]=float(line)
		print(Pi1[i])

	#Reading Class 2
	f=open("32/Class2afterGMM.txt","r")
	#Filling means of clusters of class2
	for i in range(K):
		line=next(f)
		line=line.split()
		for j in range(D):
			clusterCentres2[i][j]=float(line[j])
		print(clusterCentres2[i])
	#Filling Sigma of clusters of class1
	for i in range(K):
		line=next(f)
		line=line.split()
		for j in range(D):
			for k in range(D):
				Sigma2[i][j][k]=float(line[(j*2)+(k*1)])
		print(Sigma2[i])
	#Filling Pi of clusters of class1
	for i in range(K):
		line=next(f)
		Pi2[i]=float(line)
		print(Pi2[i])

	#Reading Class 3
	f=open("32/Class3afterGMM.txt","r")
	#Filling means of clusters of class3
	for i in range(K):
		line=next(f)
		line=line.split()
		for j in range(D):
			clusterCentres3[i][j]=float(line[j])
		print(clusterCentres3[i])
	#Filling Sigma of clusters of class3
	for i in range(K):
		line=next(f)
		line=line.split()
		for j in range(D):
			for k in range(D):
				Sigma3[i][j][k]=float(line[(j*2)+(k*1)])
		print(Sigma3[i])
	#Filling Pi of clusters of class3
	for i in range(K):
		line=next(f)
		Pi3[i]=float(line)
		print(Pi3[i])

	X=getRange()
	xmin=X[0][0]
	xmax=X[0][1]
	ymin=X[1][0]
	ymax=X[1][1]

	print ("xmin = ",xmin)
	print ("ymin = ",ymin)
	print ("xmax = ",xmax)
	print ("ymax = ",ymax)
	
	A = [0 for x in range(D)]

	print("Plotting")

	i=xmin
	while i<xmax :
		j=ymin
		while j<ymax:
			A[0]=i
			A[1]=j
			g1=calcG(Pi1,clusterCentres1,Sigma1,A)
			g2=calcG(Pi2,clusterCentres2,Sigma2,A)
			g3=calcG(Pi3,clusterCentres3,Sigma3,A)
			if g1==max(g1,g2,g3):
				plt.plot(i,j,color='#f6668f',marker='s')
			elif g2==max(g1,g2,g3):
				plt.plot(i,j,color='#33d7ff',marker='s')
			elif g3==max(g1,g2,g3):
				plt.plot(i,j,color='#75f740',marker='s')
			j+=0.07
		i+=0.07

	X1=readDataSetTraining("Class1.txt")
	for i in range(TrainingSize):
		plt.plot(X1[i][0],X1[i][1],'ro')

	X2=readDataSetTraining("Class2.txt")
	for i in range(TrainingSize):
		plt.plot(X2[i][0],X2[i][1],'bo')

	X3=readDataSetTraining("Class3.txt")
	for i in range(TrainingSize):
		plt.plot(X3[i][0],X3[i][1],'go')
	
	plt.xlim(xmin,xmax)
	plt.ylim(ymin,ymax)
	plt.savefig('32/Classification.png')


if __name__== "__main__":
	main()