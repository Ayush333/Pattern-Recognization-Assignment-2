import matplotlib.pyplot as plt
import random
import sys
import math
from mpmath import mpf, mpc, mp

#1=2291
#2=2488

CLASS_SIZE=2488
K=4
D=2

def distance(pointA,pointB):
	return(((pointA[0]-pointB[0])*(pointA[0]-pointB[0]))+((pointA[1]-pointB[1])*(pointA[1]-pointB[1])))


def main():
	mp.dfs=200
	print("Reading")
	#Reading file 
	dSet=[[0 for x in range(D+1)]for y in range(CLASS_SIZE)]
	f=open("Class2.txt","r")
	fl=f.readlines()
	i=0
	for lines in fl:
		lines=lines.split()
		for j in range(D):
			dSet[i][j]=float(lines[j])
		i+=1
	f.close()
	

	clusterCentres=[[0 for x in range(D)]for y in range(K)]
	newclusterCentres=[[0 for x in range(D+1)]for y in range(K)]
	
	#Random Allocation of Cluster Centres
	for x in range(K):
		# r=random.randint(1,CLASS_SIZE+1)
		# print(r)
		for i in range(D):
			clusterCentres[x][i]=dSet[x][i]
		
	#KMeans
	oldCost=sys.maxsize
	diff=20
	counter=1

	while diff>0.1:
		#Reallocating cluster to every point
		for x in range(CLASS_SIZE):
			min=sys.maxsize
			for y in range(K):
				if distance(clusterCentres[y],dSet[x])<min:
					min=distance(clusterCentres[y],dSet[x])
					dSet[x][D]=y
				# print(distance(clusterCentres[y],dSet[x]))
			# print(dSet[x][2])

		#Recalculating New Mean
		for x in range(CLASS_SIZE):
			newclusterCentres[dSet[x][D]][D]+=1
			for i in range(D):
				newclusterCentres[dSet[x][D]][i]+=dSet[x][i]
		for x in range(K):
			for i in range(D):
				clusterCentres[x][i]=newclusterCentres[x][i]/newclusterCentres[x][D]
		#Calculating new cost to calculate diff
		newCost=0
		for x in range(CLASS_SIZE):
			newCost+=distance(dSet[x],clusterCentres[dSet[x][D]])
		# print(newCost)
		diff=oldCost-newCost
		oldCost=newCost
		print(diff)
		counter+=1
		file=open("4/Class2afterKmeans.txt","w")
		for i in range(K):
			for j in range(D):
				file.write(str(clusterCentres[i][j]))
				file.write(" ")	
			file.write("\n")

		for i in range(CLASS_SIZE):
			for j in range(D):
				file.write(str(dSet[i][j]))
				file.write(" ")
			file.write("%d"%(dSet[i][D]))	
			file.write("\n")

	file.close
	# for i in range(CLASS_SIZE):
	# 	print(i," ",dSet[i])

	return
	#Plotting
	print("Plotting")
	for i in range(CLASS_SIZE):
		# print(dSet[i][0]," ",dSet[i][1])
		if dSet[i][D]==0:
			plt.plot(dSet[i][0],dSet[i][1],'bo')
		elif dSet[i][D]==1:
			plt.plot(dSet[i][0],dSet[i][1],'go')
		elif dSet[i][D]==2:
			plt.plot(dSet[i][0],dSet[i][1],'ro')
		elif dSet[i][D]==3:
			plt.plot(dSet[i][0],dSet[i][1],'co')
		elif dSet[i][D]==4:
			plt.plot(dSet[i][0],dSet[i][1],'mo')
		elif dSet[i][D]==5:
			plt.plot(dSet[i][0],dSet[i][1],'yo')
		elif dSet[i][D]==6:
			plt.plot(dSet[i][0],dSet[i][1],'ko')
		elif dSet[i][D]==7:
			plt.plot(dSet[i][0],dSet[i][1],'wo')
		# elif dSet[i][D]==8:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==9:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==10:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==11:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==12:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==13:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==14:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==15:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==16:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==17:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==18:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==19:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==20:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==21:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==22:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==23:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==24:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==25:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==26:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==27:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==28:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==29:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==30:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
		# elif dSet[i][D]==31:
		# 	plt.plot(dSet[i][0],dSet[i][1],color="#75f740")
	# plt.show()
	plt.savefig('Class3aferKmeans.png')	

	#Initialising Variables for guassian mixture


	
	

if __name__== "__main__":
	main()